#!/usr/bin/env python3
"""
Task 15's module
"""
from pymongo import MongoClient


def log_statistics():
    """a function that provides some stats about nginx logs"""
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total = collection.count_documents({})
    get = collection.count_documents({"method": "GET"})
    post = collection.count_documents({"method": "POST"})
    put = collection.count_documents({"method": "PUT"})
    patch = collection.count_documents({"method": "PATCH"})
    delete = collection.count_documents({"method": "DELETE"})
    path = collection.count_documents({"method": "GET", "path": "/status"})

    data = [
            { "$group":
                {"_id": "$ip",
                    "count": {"$sum": 1}
                    }
                },
            {"$sort":
                {"count": -1}
                }
            ]

    print("{:d} logs". format(total))
    print("Methods:")
    print("\tmethod GET: {:d}". format(get))
    print("\tmethod POST: {:d}". format(post))
    print("\tmethod PUT: {:d}". format(put))
    print("\tmethod PATCH: {:d}". format(patch))
    print("\tmethod DELETE: {:d}". format(delete))
    print("{:d} status check". format(path))

    print("IPs:")
    ips = collection.aggregate(data)
    a = 0
    for ip in ips:
        if a == 10:
            break
        print("\t{}: {}".format(ip.get('_id'), ip.get('count')))
        a += 1


if __name__ == "__main__":
    log_statistics()
