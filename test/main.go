package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type CapturedData struct {
	URL          string `json:"url"`
	Title        string `json:"title"`
	EntryTime    int64  `json:"entryTime"`
	RenderedHtml string `json:"renderedHtml"`
}

func dataHandler(w http.ResponseWriter, r *http.Request) {
	// Ensure the request method is POST
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Read the request body
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Could not read request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	// Unmarshal the JSON body into the CapturedData struct
	var data CapturedData
	err = json.Unmarshal(body, &data)
	if err != nil {
		http.Error(w, "Could not parse JSON", http.StatusBadRequest)
		return
	}

	// Print the received data to the console
	fmt.Printf("Received Data: %+v\n", data)

	// Save the received data to a text file
	file, err := os.OpenFile("received_data.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		http.Error(w, "Could not open file", http.StatusInternalServerError)
		return
	}
	defer file.Close()

	// Write data to the file
	_, err = file.WriteString(fmt.Sprintf("URL: %s\nTitle: %s\nEntryTime: %d\nRenderedHtml: %s\n\n",
		data.URL, data.Title, data.EntryTime, data.RenderedHtml))
	if err != nil {
		http.Error(w, "Could not write to file", http.StatusInternalServerError)
		return
	}

	// Send a JSON response back to the client
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "success",
		"message": "Data received and saved to file",
	})
}

func main() {
	// Set up the HTTP server
	http.HandleFunc("/endpoint", dataHandler)

	// Start the server on port 8080
	fmt.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
