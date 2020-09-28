package load

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

// SegKey 路段
type SegKey struct {
	From string `json:"from"`
	To   string `json:"to"`
}

// SegV 路段
type SegV struct {
	T     string `json:"type"`
	value float64
	cnt   int
	Res   float64 `json:"v"`
}

type widang struct {
	id    string
	angle float64
}

var (
	ways      map[string][]string
	wayl      map[string]map[string]string
	wayr      map[string]map[string]string
	waytype   map[string]string
	wayangle  map[string][]float64
	nodes     map[string][]float64
	nodewayid map[string][]widang
	// Tsd 按照时刻划分的数据
	Tsd map[int]map[SegKey]*SegV
)

const maxID = 7902002241

func parseJSON(f string, data interface{}) {
	fp, err := os.Open(f)
	if err != nil {
		panic(err)

	}
	defer fp.Close()
	dec := json.NewDecoder(fp)
	err = dec.Decode(data)
	if err != nil {
		panic(err)
	}
}

// LoadWays 加载道路数据
func LoadWays(f string) {
	parseJSON(f, &ways)
	fmt.Println(len(ways))
	wayl = make(map[string]map[string]string)
	wayr = make(map[string]map[string]string)
	for i := range ways {
		wayl[i] = make(map[string]string)
		wayr[i] = make(map[string]string)
		l := ways[i][0]
		for _, nd := range ways[i] {
			ind, _ := strconv.Atoi(nd)
			wayl[i][nd] = l
			if ind < maxID {
				l = nd
			}
		}
		r := ways[i][len(ways[i])-1]
		for j := len(ways[i]) - 1; j >= 0; j-- {
			nd := ways[i][j]
			ind, _ := strconv.Atoi(nd)
			wayr[i][nd] = r
			if ind < maxID {
				r = nd
			}
		}
	}

}

// LoadWayType 加载道路数据
func LoadWayType(f string) {
	parseJSON(f, &waytype)
	fmt.Println(len(waytype))
}

// LoadWayType 加载道路数据
func LoadWayAngle(f string) {
	parseJSON(f, &wayangle)
	fmt.Println(len(waytype))
}

// LoadNodes 加载道路数据
func LoadNodes(f string) {
	parseJSON(f, &nodes)
	nodewayid = make(map[string][]widang)
	for i := range ways {
		for j, nd := range ways[i] {
			if j == 0 || j == len(ways[i])-1 {
				continue
			}
			nodewayid[nd] = append(nodewayid[nd], widang{
				id:    i,
				angle: wayangle[i][j],
			})
		}
	}
}

// LoadTsd 加载堵塞数据
func LoadTsd(f string) {
	fp, err := os.Open(f)
	if err != nil {
		panic(err)
	}
	defer fp.Close()
	Tsd = make(map[int]map[SegKey]*SegV)
	reader := bufio.NewReader(fp)
	for {
		str, err := reader.ReadString('\n')
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			panic(err)
		}
		str = strings.TrimSpace(str)
		ss := strings.Split(str, ",")
		if ws, ok := nodewayid[ss[0]]; ok {
			ange, _ := strconv.ParseFloat(ss[1], 64)
			ts, _ := strconv.Atoi(ss[2])
			fact, _ := strconv.ParseFloat(ss[3], 64)
			cnt, _ := strconv.Atoi(ss[4])
			k := SegKey{}
			w := ""
			minangle := 800.0
			flag := true
			for _, xy := range ws {
				aangel := 180 + xy.angle
				if aangel >= 360 {
					aangel -= 360
				}
				zhengx := min(math.Abs(xy.angle-ange), 360-math.Abs(xy.angle-ange))
				fux := min(math.Abs(aangel-ange), 360-math.Abs(aangel-ange))
				mint := min(zhengx, fux)
				if mint < minangle {
					w = xy.id
					minangle = mint
					flag = zhengx < fux
				}
			}
			if w == "" {
				fmt.Println("未找到")
				continue
			}
			ind, _ := strconv.Atoi(ss[0])
			if flag {
				if ind < maxID {
					k.From = ss[0]
				} else {
					k.From, ok = wayl[w][ss[0]]
					if !ok {
						fmt.Println("err id:" + ss[0])
						continue
					}
				}
				k.To, ok = wayr[w][ss[0]]
				if !ok {
					fmt.Println("err id:" + ss[0])
					continue
				}
			} else {
				k.To, ok = wayl[w][ss[0]]
				if !ok {
					fmt.Println("err id:" + ss[0])
					continue
				}
				if ind < maxID {
					k.From = ss[0]
				} else {
					k.From, ok = wayr[w][ss[0]]
					if !ok {
						fmt.Println("err id:" + ss[0])
						continue
					}
				}
			}

			if _, ok := Tsd[ts]; !ok {
				Tsd[ts] = make(map[SegKey]*SegV)
			}
			if _, ok := Tsd[ts][k]; ok {
				Tsd[ts][k].value += fact
				Tsd[ts][k].cnt += cnt
			} else {
				Tsd[ts][k] = &SegV{
					value: fact,
					cnt:   cnt,
					T:     waytype[w],
				}
			}
		}

	}
	for i := range Tsd {
		for _, k := range Tsd[i] {
			k.Res = k.value / float64(k.cnt)
		}
	}
}

func min(x, y float64) float64 {
	if x < y {
		return x
	}
	return y
}
