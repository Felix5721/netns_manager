package main

import(
	"fmt"
	"os"
	"os/exec"
	"encoding/json"
	"strconv"
	"path/filepath"
)

type Netns struct {
	Name		string
	Vethip		string
	Peerip		string
	Mask		int
	DNS_IP		string
}

var start bool
var nsfile string

func readNetnsConf(file string) (Netns, error){
	var nns Netns
	f, notfound := os.Open(file)
	if notfound != nil {
		fmt.Println("Config not found exiting")
		return nns, notfound
	}
	dec := json.NewDecoder(f)
	err := dec.Decode(&nns)
	if err != nil {
		panic(err)
	}
	return nns, nil
}

func init() {
	if len(os.Args) != 3{
		fmt.Println(os.Args[0]+" start\\stop netns.json")
		os.Exit(1)
	} else {
		if os.Args[1] == "start" {
			start = true
		} else {
			start = false
		}
		nsfile = os.Args[2]
	}
}

func main(){
	netns, err := readNetnsConf(nsfile)
	if err != nil{
		os.Exit(1)
	}
	if start {
		if _, err := os.Stat("./scripts/makenets.sh"); err == nil {
			cmd := exec.Command("./scripts/makenets.sh", netns.Name, netns.Vethip, netns.Peerip, strconv.Itoa(netns.Mask))
			err := cmd.Run()
			if  err != nil{
				panic(err)
			}
		} else if _, err := os.Stat("/etc/netns_manager/scripts/makenets.sh"); err==nil{
			cmd := exec.Command("/etc/netns_manager/scripts/makenets.sh", netns.Name, netns.Vethip, netns.Peerip, strconv.Itoa(netns.Mask))
			err := cmd.Run()
			if  err != nil{
				panic(err)
			}
		} else {
			fmt.Println("Netns creation script not found")
			os.Exit(1)
		}
		resolvpath := "/etc/netns/" + netns.Name
		resolvfile := filepath.Join(resolvpath, "resolv.conf")
		if netns.DNS_IP != "" {
			os.MkdirAll(resolvpath, os.ModeDir)
			entry := fmt.Sprintf("nameserver\t%s", netns.DNS_IP)
			f, err := os.OpenFile(resolvfile, os.O_RDWR|os.O_CREATE, 0755)
			if err != nil{
				panic(err)
			}
			defer f.Close()
			f.WriteString(entry)
		} else {
			if _, err := os.Stat(resolvfile); err == nil {
				os.Remove(resolvfile)
			}
		}
	} else {
		cmd := exec.Command("ip", "netns", "delete", netns.Name)
		err := cmd.Run()
		if  err != nil{
			panic(err)
		}
	}
}
