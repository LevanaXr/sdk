from sdk.API import API
from sdk.data.CANFrame import CANFrame
from sdk.data.CANResponseFilter import CANResponseFilter
from sdk.data.Query import Query
from sdk.data.Request import Request

if __name__ == "__main__":
    # use test api key and secret
    key = "700fb92b-1505-4a39-9b08-927cbe0257d6"
    secret = "47ac4af9-ed2a-4ed0-8d59-d431162a3032"
    # create api connection
    api = API()
    # get authentication token
    token = api.authenticate(key, secret)

    # get available devices, Device.TEST_DEVICE is always available
    devices = api.get_connected_devices(token)
    # find available device
    device = None
    for dev in devices:
        if dev.is_available_now():
            device = dev
            print("Selected car: " + device.name)
            break

    # connect to it
    cloud = api.connect_to_device(token, device)

    # create CAN frame, with id 0x700 and data
    can_frame = CANFrame(0x700, bytearray([0x1]))
    # create request to send the can frame
    # and collect all responses from CAN bus for 300 ms
    request = Request(can_frame, 300)
    try:
        can_query = Query([request], CANResponseFilter.NONE())
        responses = cloud.send_can_query(can_query)
        for response in responses:
            frame_ids = {hex(x.frame_id) for x in response.iterator()}
            print("Request ID: " + hex(response.request.frame_id))
            print("Unique ids: " + str(len(frame_ids)))
            print("IDs: " + str(frame_ids))
    finally:
        cloud.close()