package main

import (
	"data/api"
	"data/load"
	"data/middleware"

	"github.com/gin-gonic/gin"
)

var tsdf = []string{
	"./source/1001/000000_0",
	/*	"./source/1002/000000_0",
		"./source/1003/000000_0",
		"./source/1004/000000_0",
		"./source/1005/000000_0",
		"./source/1006/000000_0",
		"./source/1007/000000_0",*/
}

func main() {

	load.LoadWays("./source/ways.json")
	load.LoadWayType("./source/waytype.json")
	load.LoadWayAngle("./source/wayangel.json")
	load.LoadNodes("./source/nodes.json")
	for _, i := range tsdf {
		load.LoadTsd(i)
	}

	var Router = gin.Default()
	Router.Static("source", "./source")
	Router.Use(middleware.Cors()) // 跨域

	APIGroup := Router.Group("")
	// GET /way?ts=xx
	APIGroup.GET("way", api.Way)
	Router.Run(":1234")
}
