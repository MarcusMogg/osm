package api

import (
	"data/load"
	"data/response"
	"strconv"

	"github.com/gin-gonic/gin"
)

// Way 根据时间戳获取对应时刻的拥堵数据
func Way(c *gin.Context) {
	ts, err := strconv.Atoi(c.DefaultQuery("ts", "0"))
	if err != nil {
		response.FailValidate(c)
		return
	}
	res := load.Tsd[ts]
	var r []gin.H
	for i, j := range res {
		r = append(r, gin.H{
			"k": i,
			"v": *j,
		})
	}
	response.OkWithData(r, c)
}
