package logger

import (
	"fmt"
	"net/http"
	"strings"
)

const larkBotWebhookURL = "https://open.feishu.cn/open-apis/bot/v2/hook/61f8efec-d13b-47a6-8366-697b5db500ec"

func LogMessage(logType string, logContent string) {
	go func() {
		msg := fmt.Sprintf("{\"msg_type\": \"text\", \"content\": {\"text\":\"[%s] %s\"}}", strings.ToUpper(logType), logContent)
		_, err := http.Post(larkBotWebhookURL, "application/json", strings.NewReader(msg))
		if err != nil {
			fmt.Println(err)
			return
		}
	}()

}
