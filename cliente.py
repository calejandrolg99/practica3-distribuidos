import sys
import time
from kazoo.client import KazooClient

zk = KazooClient(hosts=f"{sys.argv[1]}:{sys.argv[2]}")
zk.start()
zk.ensure_path("/app/group")
zk.create(
    "/app/group/node_", ephemeral=True, sequence=True, value=str([sys.argv[3]]).encode()
)

counting_child = ""
id_counting_child = ""
next_counting_child = ""
id_next_counting_child = ""


def to_array(value):
    arr = value.split(", ")
    arr = [v.strip("['']") for v in arr]
    return arr


def watch_counting_child(
    data,
    stat,
):
    if data:
        value = to_array(data.decode())
        value[0] = sys.argv[3]
        print("La cuenta va por: ", value[1])
        zk.set("/app/group/" + next_counting_child, str(value).encode())


@zk.ChildrenWatch("/app/group")
def watch_children(children):
    global next_counting_child
    global id_next_counting_child
    global counting_child
    global id_counting_child
    count = 0

    children = sorted(children)
    counting_child = children[0]
    id_counting_child = to_array(zk.get("/app/group/" + counting_child)[0].decode())[0]

    if len(children) > 1:
        next_counting_child = children[1]
        id_next_counting_child = to_array(
            zk.get("/app/group/" + next_counting_child)[0].decode()
        )[0]
    elif len(children) == 1:
        next_counting_child = ""
        id_next_counting_child = ""

    if zk.get("/app/group/" + counting_child)[0].decode():
        value = to_array(zk.get("/app/group/" + counting_child)[0].decode())

        if len(value) == 1:
            count = 0
        else:
            count = int(value[1])

    print("#####################")
    print("Nodos: ", children)
    print("Identificador: ", sys.argv[3])
    print("Nodo contador: ", counting_child)
    print("Nodo siguiente: ", next_counting_child)
    print("#####################")

    if sys.argv[3] == id_counting_child:
        while True:
            value = to_array(zk.get("/app/group/" + counting_child)[0].decode())

            if len(value) == 1:
                value.append(count)
            else:
                value[1] = count

            zk.set("/app/group/" + counting_child, str(value).encode())
            print("Contador: ", count)
            count += 1
            time.sleep(1)
    else:
        zk.DataWatch(
            "/app/group/" + counting_child,
            watch_counting_child,
        )


while True:
    time.sleep(1)
