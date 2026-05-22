package main

import (
	"fmt"
	"os"
	"net/http"
	"bufio"
	"strings"
	"log"
	"sync"
)

func parseUrl(url string) string {
	return "http://" + url
}

func sendRequest(url string) {
	request, err := http.Get(url)
	if err != nil {
		fmt.Println("Error sending the request %s: %s",url, err)
	}
	if request.StatusCode == 200 {
		fmt.Println("Directory %s exists and is accessible", url)
	} else if request.StatusCode == 404 {
		fmt.Println("Directory %s Not Found", url)
	} else if request.StatusCode == 403 {
		fmt.Println("Directory %s exists but is not accessible", url)
	}

}
func bruteforce(url string, wordlist string) {
	var wg sync.WaitGroup
	file, err := os.Open(wordlist)
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			dirNameUnstripped := scanner.Text()
			dirName := strings.TrimSpace(dirNameUnstripped)
			wg.Add(1)
			go func(d string) {
				defer wg.Done()
				sendRequest(url + "/" + d)
			} (dirName)
		}
		wg.Wait()
		if err := scanner.Err(); err != nil {
			log.Fatalf("error reading file: %s", err)
		}

	}

func main() {
	url := parseUrl(os.Args[1])
	wordlist := os.Args[2]

	bruteforce(url, wordlist)
}
