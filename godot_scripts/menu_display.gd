extends Control

# Menu display configuration
var menu_items = []
var menu_container
var http_request = HTTPRequest.new()

func _ready():
    # Add HTTP request node
    add_child(http_request)
    http_request.request_completed.connect(_on_request_completed)
    
    # Initialize menu container
    menu_container = $MenuContainer
    if not menu_container:
        print("Error: MenuContainer node not found!")
        return
    
    # Fetch menu from API
    fetch_menu()

func fetch_menu():
    var error = http_request.request("http://localhost:8000/menu")
    if error != OK:
        print("Failed to request menu data")

func _on_request_completed(result, response_code, headers, body):
    if response_code == 200:
        var json = JSON.parse_string(body.get_string_from_utf8())
        if json:
            menu_items = json
            update_menu_display()

func update_menu_display():
    # Clear existing menu items
    for child in menu_container.get_children():
        child.queue_free()
    
    # Create menu items
    for item_id, item in menu_items.items():
        var menu_item = create_menu_item(item_id, item)
        menu_container.add_child(menu_item)

func create_menu_item(item_id, item):
    var container = HBoxContainer.new()
    container.set_h_size_flags(Control.SIZE_EXPAND_FILL)
    
    # Item name and price
    var label = Label.new()
    label.text = "%s - $%.2f" % [item["name"], item["price"]]
    container.add_child(label)
    
    # Add some spacing
    container.add_spacer(false)
    
    return container

# Function to display an image in the menu
func display_image(image_path: String, image_node: TextureRect) -> void:
    var image = Image.load_from_file(image_path)
    if image:
        var texture = ImageTexture.create_from_image(image)
        image_node.texture = texture
    else:
        print("Failed to load image: ", image_path) 