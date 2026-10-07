# HTTP

!!! Warning "Internal API"
    These classes are for internal use only.
    
    Users should interact with [Client](../api/client.md) and other public [API](../api/index.md) classes instead.
---

```
Key:
	A:B = map
	[A] = step
	[A]-->[B] = flow
	[A]--|N|-->[B] = flow using N
	F(X) = input X, output F

R = request
EP = endpoint
L = Lock
Q = Queue
H = header
B = bucket

HTTP(EP) = [R:EP]--|L|-->[Q:EP]--|send R|-->[add/update H:B]
```

:::scurrypy.core.http
