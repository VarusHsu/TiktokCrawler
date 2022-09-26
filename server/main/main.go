package main

import (
	"bufio"
	"draft/logger"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"io/fs"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

type ListType int32

const (
	ListTypeInvalid    ListType = 0
	ListTypeByTime     ListType = 1
	ListTypeByIncrease ListType = 2
)

type listHistoryResponse struct {
	ListType string   `json:"listType"`
	Items    []string `json:"items"`
}

func main() {
	r := gin.Default()
	logger.LogMessage("START", "Crawl service start.")

	r.POST("/upload", handlePostUpload)
	r.GET("/ping", handleGetPing)
	r.GET("/list_history_by_time", handleGetListHistoryByTime)
	r.GET("/list_history_by_increase", handleGetListHistoryByIncrease)
	r.GET("/download", handleGetDownload)

	err := r.Run()
	if err != nil {
		content := fmt.Sprintf("Gin run error.")
		logger.LogMessage("ERROR", content)
		return
	}

}

func handlePostUpload(context *gin.Context) {
	file, headers, err := context.Request.FormFile("file")
	if err != nil {
		context.String(http.StatusBadRequest, "Bad request")
		content := fmt.Sprintf("Post '%s' error, %s", "upload", err)
		logger.LogMessage("ERROR", content)
		return
	}
	filename := headers.Filename
	out, err := os.Create("/home/ubuntu/TiktokCrawler/server/source/" + filename)
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
	logger.LogMessage("SERVER", "Interface: PostUpload")
	setSourcePath(filename)
	context.String(http.StatusCreated, "Upload Success")
}

func handleGetPing(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
	logger.LogMessage("SERVER", "Interface: GetPing.")
}

func handleGetListHistoryByTime(context *gin.Context) {
	context.JSON(http.StatusOK,
		listHistoryResponse{
			ListType: "time",
			Items:    getList(ListTypeByTime),
		})
	logger.LogMessage("SERVER", "Interface: GetListHistoryByTime.")
}

func handleGetListHistoryByIncrease(context *gin.Context) {
	context.JSON(http.StatusOK,
		listHistoryResponse{
			ListType: "increase",
			Items:    getList(ListTypeByIncrease),
		})
	logger.LogMessage("SERVER", "Interface: GetListHistoryByIncrease.")
}

func getList(listType ListType) []string {
	files := make([]string, 0)
	var path string
	if listType == ListTypeByTime {
		path = "./history/by_time/"
	} else if listType == ListTypeByIncrease {
		path = "./history/by_increase/"
	} else {
		logger.LogMessage("ERROR", "Get list error list type.")
		return nil
	}
	err := filepath.Walk(path, func(path string, info fs.FileInfo, err error) error {
		if path == "./history/by_time/" || path == "./history/by_increase/" {
			return nil
		} else {
			path = strings.Replace(path, "history/by_time/", "", 1)
			path = strings.Replace(path, "history/by_increase/", "", 1)
		}
		if path != ".gitkeep" && path != "nohup.out" {
			files = append(files, path)
		}
		return nil
	})
	if err != nil {
		content := fmt.Sprintf("Get list walk error %s", err)
		logger.LogMessage("ERROR", content)
		return nil
	}
	return files
}

func handleGetDownload(context *gin.Context) {
	listTypeInt, err := strconv.Atoi(context.Query("list_type"))
	if err != nil {
		content := fmt.Sprintf("Get download atoi error %s", err)
		logger.LogMessage("ERROR", content)
		return
	}
	listType := ListType(listTypeInt)
	fileName := context.Query("filename")
	var path string
	switch listType {
	case ListTypeByTime:
		path = "./history/by_time/"
	case ListTypeByIncrease:
		path = "./history/by_increase/"
	default:
		logger.LogMessage("ERROR", "Get download unknown list type")
		context.JSON(http.StatusBadRequest, "Bad Request")
		return
	}
	fullPath := path + fileName
	_, err = os.Stat(fullPath)
	if err != nil {
		context.JSON(http.StatusNotFound, "No Such file")
		return
	}
	context.File(fullPath)
	logger.LogMessage("SERVER", "Interface: GetDownload.")
	return
}

func setSourcePath(fileName string) {
	filePath := "/home/ubuntu/TiktokCrawler/scheduler_job/source.py"
	_ = os.Remove(filePath)
	file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE, 0666)
	if err != nil {
		logger.LogMessage("ERROR", "Open file error.")
	}
	defer file.Close()
	code := fmt.Sprintf("source_path = '/home/ubuntu/TiktokCrawler/server/source/%s\n'", fileName)
	writer := bufio.NewWriter(file)
	_, err = writer.WriteString(code)
	if err != nil {
		logger.LogMessage("ERROR", "Write source path error.")
		return
	}
	err = writer.Flush()
	if err != nil {
		logger.LogMessage("ERROR", "Write source path flush error.")
		return
	}
}
