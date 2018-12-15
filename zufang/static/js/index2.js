//**创建地图,同时给地图设置中心点、级别、显示模式、自定义样式等属性：
var map = new AMap.Map("container", {
    resizeEnable: true,
    zoomEnable: true,
    center:  [113.244261,23.125981],
    zoom: 11
});

//**创建地图比例尺插件
var scale = new AMap.Scale();

//**比例尺插件添加到地图
map.addControl(scale);

/***AMap.ArrivalRange根据输入的起点坐标和设定的时间范围，
可以计算出用户在你设定的时间段内按公交出行方式，可以到达的距离范围。
用户可以通过自定义回调函数取回并显示查询结果。
若服务请求失败，系统将返回错误信息。*/
var arrivalRange = new AMap.ArrivalRange();
var x, y, t, vehicle = "SUBWAY,BUS";
var workAddress,workMarker;
var rentMarkerArray = [];
var polygonArray = [];
var amapTransfer;
//workAddress="广州火车站"
//**新建信息窗体
var infoWindow = new AMap.InfoWindow({
    offset: new AMap.Pixel(0, -30)
});

//**关键词匹配
var auto = new AMap.Autocomplete({
    input: "work-location"
});

//**添加监听事件
AMap.event.addListener(auto, "select", workLocationSelected);

//loadWorkLocation:定位并标记
function takeBus(radio) {
    vehicle = radio.value;
    loadWorkLocation()
}

function takeSubway(radio) {
    vehicle = radio.value;
    loadWorkLocation()
}


//**poi:根据关键字获取对应城市里相关的POI信息
function workLocationSelected(e) {
    workAddress = e.poi.name;
    loadWorkLocation();
}

//**AMap.Marker:创建标记
function loadWorkMarker(x, y, locationName) {
    workMarker = new AMap.Marker({
        map: map,
        title: locationName,
        icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
        position: [x, y]

    });
}

//**1.arrivalRange.search:计算某个时间段内用户通过公交出行可到达的距离范围
//**2.AMap.Polygon:添加多边形对象
function loadWorkRange(x, y, t, color, v) {
    arrivalRange.search([x, y], t, function(status, result) {
        if (result.bounds) {
            for (var i = 0; i < result.bounds.length; i++) {
                var polygon = new AMap.Polygon({
                    map: map,
                    fillColor: color,
                    fillOpacity: "0.4",
                    strokeColor: color,
                    strokeOpacity: "0.8",
                    strokeWeight: 1
                });
                polygon.setPath(result.bounds[i]);
                polygonArray.push(polygon);
            }
        }
    }, {
        policy: v
    });
}

/**1.AMap.Transfer:公交换乘服务，提供起始点公交路线规划服务，
目前公交换乘仅支持同一城市的公交路线规划*/
//**amapTransfer.search根据起点和终点坐标/名称，进行公交换乘查询；
function addMarkerByAddress(address,houseInfo,price,link,workAddress) {
    var geocoder = new AMap.Geocoder({
        radius: 1000
    });
    geocoder.getLocation(address,function(status, result) {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            rentMarker = new AMap.Marker({
                map: map,
                title: address,
                icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
                position: [geocode.location.getLng(), geocode.location.getLat()]
            });
            rentMarkerArray.push(rentMarker);
            rentMarker.content = "<div>房源基本信息："+ houseInfo + "<div>"+
                                "<div>房源地址："+ address + "<div>"+
                                "<div>房价："+ price + "<div>"+
                                "<div><a target = '_blank' href='" +link+ "'>"+"房源链接"+"</a><div>"
            
            rentMarker.on('click', function(e) {
                infoWindow.setContent(e.target.content);
                infoWindow.open(map, e.target.getPosition());
                if (amapTransfer) amapTransfer.clear();
                amapTransfer = new AMap.Transfer({
                    map: map,
                    policy: AMap.TransferPolicy.LEAST_TIME,
                    city: "广州市",
                    panel: 'transfer-panel'
                });
                amapTransfer.search([{
                    keyword: workAddress
                }, {
                    keyword: address
                }], function(status, result) {})
            });
        }
    })
}
//**map.remove:删除定位区域及标记
function delWorkLocation() {
    if (polygonArray) map.remove(polygonArray);
    if (workMarker) map.remove(workMarker);
    polygonArray = [];
}

function delRentLocation() {
    if (rentMarkerArray) map.remove(rentMarkerArray);
    rentMarkerArray = [];
}


//**1.AMap.Geocoder:地理描述与坐标之间的转换
//**2.getLocation:解析地理描述获取定位
//**3.getLng,getLat:获取经纬度
//**4.loadWorkMarker:添加标记
//**5.loadWorkRange:添加工作范围附近区域
//**6.setZoomAndCenter:地图缩放至指定级别并以指定点为地图显示中心点
//**7.delWorkLocation:删除工作定位
function loadWorkLocation() {
    delWorkLocation();
    var geocoder = new AMap.Geocoder({
        city: "广州",
        radius: 1000
    });

    geocoder.getLocation(workAddress, function(status, result) {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            x = geocode.location.getLng();
            y = geocode.location.getLat();
            loadWorkMarker(x, y);
            loadWorkRange(x, y, 60, "#3f67a5", vehicle);
            map.setZoomAndCenter(12, [x, y]);
        }
    })
}
