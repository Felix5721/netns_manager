package main

import(
	"fmt"
	"os"
	"encoding/json"
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
	fmt.Println(netns.Name)
}
