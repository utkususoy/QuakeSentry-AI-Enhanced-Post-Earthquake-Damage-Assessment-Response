from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .config.database import DamagedIdentificationDB
# from .config.model import Tweet, UpdateTweetType
import json
import asyncio
from pydantic import BaseModel
from kafka import KafkaConsumer

from aiokafka import AIOKafkaConsumer
import asyncio

app = FastAPI()
db_con = DamagedIdentificationDB()
origins = [
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# TODO: 
# 1) ilk açılışta db den alcak (DONE)
# 2) güncel yeni verileri websocketten alacak

class Tweet(BaseModel):
    tweet_uuid_: str

# consumer = KafkaConsumer('damaged-tweets',  # topic to consume from
#     bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'],  # Kafka broker addresses
#     group_id='my-group',  # consumer group ID
#     auto_offset_reset='earliest',  # start consuming from earliest available message
#     enable_auto_commit=True  # commit offsets automatically after consuming messages
#     )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer('damaged-tweets', loop=loop,
                                bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'],  # Kafka broker addresses
                                  # consumer group ID
                                )
    payloads = db_con.fetch_valid_address()
    await consumer.start()
    
    try:
       # while True:
        async for message in consumer:
            # print("sending...")
            # print(message.value.decode("utf-8"))
            message_value = message.value.decode("utf-8")
            json_data = json.loads(message_value)
            if json_data["geo_code"]:
                await websocket.send_json(json_data)
        

        # for i in payloads:
        #     if i["geo_code"]:
        #         await websocket.send_json(i)
        #         await asyncio.sleep(1)
    except WebSocketDisconnect as e:
        print("@Errorr")
        print(e)
    # #     await asyncio.sleep(0.1)
        # try:
        #     await websocket.send_text(message.value.decode("utf-8"))
        # except WebSocketDisconnect:
        #     break
    # counter = 0
    # while True:
    #     # Send data to the client
    #     data = {"message": f"Hello, number of {counter} client!"}
    #     await websocket.send_json(data)
    #     print("heheeee")
    #     # Delay before sending the next message
    # #    await asyncio.sleep(1)
    #     counter += 1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/locations")
async def get_locations():
   payload = db_con.fetch_valid_address()
#    payload = []
   return payload
    # return ""

#TODO: Convert http method to delete.
@app.post("/remove-tweet")
async def remove_tweet(tweet_uuid_ : Tweet):
    print(tweet_uuid_.tweet_uuid_)
    db_con.remove_tweet_by_uuid(tweet_uuid_.tweet_uuid_)

@app.post("/change-tweet-type")
async def change_tweet_type(request : Request):
    payload = await request.json()
    print("hereeeee")
    print(payload)
    db_con.update_tweet_type(payload["tweet_uuid"], payload["label"])

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}