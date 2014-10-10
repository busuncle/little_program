import os
import urllib2
import socket
import cStringIO
import Image
import redis
import config as cfg

BASE_PATH = "uwsgi"

HTTP_STATUS = {
    200: "200 OK",
    404: "404 Not Found",
}



red = redis.StrictRedis(host=cfg.REDIS.HOST, port=cfg.REDIS.PORT, db=cfg.REDIS.DB)


def _get_child_path(path_info):
    path_list = path_info.split("/")
    res = []
    for path in path_list:
        if path == BASE_PATH or len(path) == 0:
            continue
        res.append("/" + path)

    return "".join(res)


def _get_params(query_string):
    params = query_string.split("&")
    res = {}
    for p in params:
        k, v = p.split("=")
        res[k] = v

    return res



def resize_img(img_url, w, h, save_type="PNG"):
    # image resize
    cache_time = 3600 * 24 * 30
    img_cache = red.get(img_url)
    if img_cache is not None:
        #print "%s is in redis" % img_url
        return {"code": 1, "new_img": img_cache}

    w, h = int(w), int(h)
    if w <= 0 or h <= 0:
        return {"code": -1, "new_img": None}

    new_size = (w, h)
    try:
        req = urllib2.urlopen(img_url, timeout=30)
        cont = req.read()
    except urllib2.URLError, err:
        if isinstance(err.reason, socket.timeout):
            return {"code": -1, "new_img": None}

    fp = cStringIO.StringIO(cont)
    img = Image.open(fp)

    new_img = img.resize(new_size)
    output_fp = cStringIO.StringIO()
    new_img.save(output_fp, save_type)
    img_cache = output_fp.getvalue()
    output_fp.close()

    red.set(img_url, img_cache)
    red.expire(img_url, cache_time)
    return {"code": 1, "new_img": img_cache}



def application(env, start_response):
    # entrance
    response_status = HTTP_STATUS[200]
    response_headers = []
    child_path = _get_child_path(env["PATH_INFO"])
    params = _get_params(env["QUERY_STRING"])
    response_body = ""
    if child_path == "/resize_img":
        res = resize_img(params["img_url"], params["w"], params["h"])
        if res["code"] == 1:
            response_headers.append(('Content-Type','image/jpeg'))
            response_body = res["new_img"]
        else:
            response_status = HTTP_STATUS[404]

    start_response(response_status, response_headers)
    return [response_body]



if __name__ == "__main__":
    print "==================== test begin =========================="
    #print _get_child_path("/uwsgi/img")
    print _get_params("url=http://www.baidu.com")
    print "==================== test end =========================="
