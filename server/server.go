package main

import (
	"draft/logger"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"net/http"
	"os"
)

func main() {
	r := gin.Default()
	logger.LogMessage("START", "Crawl service start.")
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
			content := fmt.Sprintf("Post '%s' error, %s", "upload", err)
			logger.LogMessage("ERROR", content)
			return
		}
		filename := headers.Filename
		out, err := os.Create(filename)
		if err != nil {
			content := fmt.Sprintf("Create file error %s", err)
			logger.LogMessage("ERROR", content)
			return
		}
		defer out.Close()
		_, err = io.Copy(out, file)
		if err != nil {
			content := fmt.Sprintf("Copy file error %s", err)
			logger.LogMessage("ERROR", content)
			return
		}
		content := fmt.Sprintf("Update xlsx success")
		logger.LogMessage("UPDATE", content)
		context.String(http.StatusCreated, "Upload Success")
	})
	err := r.Run()
	if err != nil {
		content := fmt.Sprintf("Gin run error.")
		logger.LogMessage("ERROR", content)
		return
	}

}
