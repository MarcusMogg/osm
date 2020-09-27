package main

import (
	"data/api"
	"data/load"
	"data/middleware"

	"github.com/gin-gonic/gin"
)

var tsdf = []string{"1001"}

func main() {

	load.LoadWays("ways.json")
	load.LoadWayType("waytype.json")
	load.LoadWayAngle("wayangel.json")
	load.LoadNodes("nodes.json")
	for _, i := range tsdf {
		load.LoadTsd(i)
	}

	var Router = gin.Default()

	Router.Use(middleware.Cors()) // 跨域

	APIGroup := Router.Group("")
	// GET /way?ts=xx
	APIGroup.GET("way", api.Way)
	Router.Run(":1234")
}
