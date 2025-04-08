extends Node

# API Configuration
const API_URL = "ws://localhost:8000/ws"
const MENU_URL = "http://localhost:8000/menu"

# UI Elements
var menu_items = []
var current_order = []
var websocket = WebSocketPeer.new()
var is_connected = false

func _ready():
    # Initialize UI elements
    setup_ui()
    # Connect to the API
    connect_to_api()

func setup_ui():
    # This is where you would set up your UI elements
    # You'll need to manually create these in the Godot editor
    pass

func connect_to_api():
    var error = websocket.connect_to_url(API_URL)
    if error != OK:
        print("Failed to connect to WebSocket")
        return
    is_connected = true

func _process(_delta):
    if is_connected:
        websocket.poll()
        var state = websocket.get_ready_state()
        if state == WebSocketPeer.STATE_OPEN:
            while websocket.get_available_packet_count() > 0:
                var packet = websocket.get_packet()
                handle_response(packet.get_string_from_utf8())
        elif state == WebSocketPeer.STATE_CLOSED:
            var code = websocket.get_close_code()
            var reason = websocket.get_close_reason()
            print("WebSocket closed with code: %d, reason: %s" % [code, reason])
            is_connected = false

func handle_response(response_text):
    var response = JSON.parse_string(response_text)
    if response:
        # Update UI with response
        update_dialogue(response["text"])
        # Play voice response
        play_voice(response["voice"])
        # Update order display
        update_order_display(response["current_order"])

func update_dialogue(text):
    # Update the dialogue text in your UI
    # You'll need to implement this based on your UI setup
    pass

func play_voice(voice_data):
    # Play the voice response using Cartesia's audio data
    # You'll need to implement this based on your audio setup
    pass

func update_order_display(order):
    current_order = order
    # Update the order display in your UI
    # You'll need to implement this based on your UI setup
    pass

func send_audio_data(audio_data):
    if is_connected:
        var data = {
            "text": audio_data
        }
        websocket.send_text(JSON.stringify(data))

func _exit_tree():
    if is_connected:
        websocket.close() 