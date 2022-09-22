package main

import (
	"github.com/gin-gonic/gin"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	r.GET("/test", func(context *gin.Context) {
		context.File("../test.py")
	})
	r.POST("/upload", func(context *gin.Context) {
		file, headers, err := context.Request.FormFile("file")
		if err != nil {
			context.String(http.StatusBadRequest, "Bad request")
			return
		}
		filename := headers.Filename
		out, err := os.Create(filename)
		if err != nil {
			log.Fatal("Error")
			return
		}
		defer out.Close()
		_, err = io.Copy(out, file)
		if err != nil {
			return
		}
		context.String(http.StatusCreated, "Upload Success")
	})
	err := r.Run()
	if err != nil {
		return
	}

}
