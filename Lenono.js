const axios = require('axios');
const notify = require("./friendNotify");

async function main() {
    const timestamp = getMillisecondTimeStamp();
    const url = `https://papi.lenovo.com.cn/stock/info.jhtm?callback=jQueryJSONP_info&proInfos=%5B%7B%22activityType%22%3A+9%2C+%22productCode%22%3A1027121%2C%22personalMake%22%3A+false%7D%5D&_=${timestamp}`;

    try {
        const response = await axios.get(url);

        if (response.status === 200) {
            const data = response.data;
            const res = jsonp_decode(data);
            const num = (res.stocks && res.stocks[0] && res.stocks[0].salesNumber) || 0;
            console.log(`QQ音乐库存：${num}`);
            if (num > 0) {
                notify.BarkNotify("联想QQ音乐有库存了", num);
            }
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

function jsonp_decode(jsonp) {
    if (jsonp[0] !== '[' && jsonp[0] !== '{') {
        jsonp = jsonp.substring(jsonp.indexOf('(') + 1, jsonp.lastIndexOf(')'));
    }
    return JSON.parse(jsonp);
}

function getMillisecondTimeStamp() {
    return new Date().getTime();
}

main();
