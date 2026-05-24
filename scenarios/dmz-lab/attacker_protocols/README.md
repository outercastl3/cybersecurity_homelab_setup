# The Attacker Section of DMZ Scenario

In this section, I will provide a detailed walkthrough of my attack chains, with explanations of each tool used.

## Planned
- Login brute-force attack
- XSS attacks
- Website enumeration

## Tools Created
- Python login brute-force script
  - Collects tokens and tries each possibility from two wordlists
- Simplified threaded directory enumeration tool in Go
  - Sends GET requests to directory names from a wordlist and parses different return codes into human-readable form

## Author
Bogdan Ermakov
