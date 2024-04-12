const CryptoJS = require("crypto-js");
c = require("crypto-js")

function encrypt(e) {
    let t, n, o, i, s, r, u, l, d = Date.now(), g = "tMFw=RXrEF7y^=7QXy2h2C_g_^",
        f = (n = "YYYY-MM-DD hh:mm:ss", o = (t = (t = d) ? new Date(t) : new Date).getFullYear(), i = t.getMonth() + 1, s = t.getDate(), r = t.getHours(), u = t.getMinutes(), l = t.getSeconds(), n.replaceAll(/(?:YYYY)|(?:MM)|(?:DD)|(?:hh)|(?:mm)|(?:ss)/g, (function (e) {
            switch (e) {
                case"YYYY":
                    return o;
                case"MM":
                    return i >= 10 ? i : "0".concat(i);
                case"DD":
                    return s >= 10 ? s : "0".concat(s);
                case"hh":
                    return r >= 10 ? r : "0".concat(r);
                case"mm":
                    return u >= 10 ? u : "0".concat(u);
                case"ss":
                    return l >= 10 ? l : "0".concat(l)
            }
        })));
    d = Math.floor(d / 1e3);
    let p = c.MD5(g + f + d).toString().substring(8, 24);
    p = c.enc.Utf8.parse(p);
    let h = c.MD5(f + d + g).toString().substring(8, 24);
    h = c.enc.Utf8.parse(h);
    let w = c.enc.Utf8.parse(JSON.stringify(e));

    let encode = c.AES.encrypt(w, p, {iv: h, mode: c.mode.CBC, padding: c.pad.ZeroPadding}).toString()
    return {
        "t": d,
        "bd": 2617,
        "encode": encode
    }
}

function decrypt(d, encode) {
    let t, n, o, i, s, r, u, l
    let g = "tMFw=RXrEF7y^=7QXy2h2C_g_^"
    let f = (n = "YYYY-MM-DD hh:mm:ss", o = (t = (t = d) ? new Date(t) : new Date).getFullYear(), i = t.getMonth() + 1, s = t.getDate(), r = t.getHours(), u = t.getMinutes(), l = t.getSeconds(), n.replaceAll(/(?:YYYY)|(?:MM)|(?:DD)|(?:hh)|(?:mm)|(?:ss)/g, (function (e) {
        switch (e) {
            case"YYYY":
                return o;
            case"MM":
                return i >= 10 ? i : "0".concat(i);
            case"DD":
                return s >= 10 ? s : "0".concat(s);
            case"hh":
                return r >= 10 ? r : "0".concat(r);
            case"mm":
                return u >= 10 ? u : "0".concat(u);
            case"ss":
                return l >= 10 ? l : "0".concat(l)
        }
    })));
    d = Math.floor(d / 1e3);

    let p = c.MD5(g + f + d).toString().substring(8, 24);
    p = c.enc.Utf8.parse(p);

    let h = c.MD5(f + d + g).toString().substring(8, 24);
    h = c.enc.Utf8.parse(h);

    // 解密数据
    let decrypted = c.AES.decrypt(encode, p, { iv: h, mode: c.mode.CBC, padding: c.pad.ZeroPadding });

    // 将解密后的数据转换为原始字节数组
    let w = decrypted.toString(c.enc.Utf8);

    console.log(w);
}


let e = {
    "is_overall_sequence": 1,
    "token": "H3oijMaVT0CLtQ7ftn9f0b8S6XxZQjsgnJkji6RgrxaU1qAEoMNJMp/voZqjO+WgjPU8QIUqvlddAm5TsI0VIzps2EAI6LbqBrMBoIXsVOQGUeER4LvkXypU8vJLxWBSBzorGbVMuDCDDxKedH7q5LyzSQIGDST/vUl5dPQvE7uzQLtbJneMZIo1x5X4jSmqMROn/glwdqn3OIXfU/KDa0re/SWGASVAD/mIPJ0p1/aJGM9WCMG4dAQgovdpba+e",
    "b": 2617,
    "lat": "30.551491156684026",
    "lng": "104.05964762369791"
}
// let params = encrypt(e)
// console.log(params)


// 参数解密, 第一个参数为13位时间戳，第二个参数为抓包encode的值，这两个值抓包获取，主要是为了获取到解密参数
// decrypt()

async function fetchData(itemId) {
    let e = {
        "is_overall_sequence": 1,
        "token": "H3oijMaVT0CLtQ7ftn9f0b8S6XxZQjsgnJkji6RgrxaU1qAEoMNJMp/voZqjO+WgjPU8QIUqvlddAm5TsI0VIzps2EAI6LbqBrMBoIXsVOQGUeER4LvkXypU8vJLxWBSBzorGbVMuDCDDxKedH7q5LyzSQIGDST/vUl5dPQvE7uzQLtbJneMZIo1x5X4jSmqMROn/glwdqn3OIXfU/KDa0re/SWGASVAD/mIPJ0p1/aJGM9WCMG4dAQgovdpba+e",
        "b": 2617,
        "lat": "30.551491156684026",
        "lng": "104.05964762369791"
    }
    try {
        const response = await fetch('https://m.pailifan.com/xcx/v2/mall_v2_goods_list', {
            method: 'POST',
            body: JSON.stringify(encrypt(e))
        });
        let data = await response.json()
        if (response.status === 200) {
            let exchange = data.data.exchange
            let final_str = "";
            exchange.forEach(item => {
                let sku_name = item["sku_name"];
                let left_stock = item["left_stock"];
                if(sku_name === "腾讯QQ音乐豪华绿钻月卡" || sku_name === "腾讯视频会员月卡") {
                    if(left_stock > 0) {
                        final_str += sku_name + " : " + left_stock + "\n";
                    }
                }
            })
            console.log(final_str)

        } else {
            console.log("获取蒙牛库存异常")
        }
    } catch (error) {
        console.log("获取蒙牛库存异常")
        console.log(error)
    }
}

fetchData();
