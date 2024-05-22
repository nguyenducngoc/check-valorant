import pynput.mouse
import pyautogui
# Lưu trạng thái của chuột
mouse_state = {"left": False, "right": False}

# Hàm xử lý sự kiện nhấn chuột
def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.left:
        mouse_state["left"] = pressed
    elif button == pynput.mouse.Button.right:
        mouse_state["right"] = pressed
    # Nếu cả hai nút chuột đều được nhấn
    if mouse_state["left"] and mouse_state["right"]:
        # Thực hiện hành động kéo cửa sổ
        for i in range(1,5):
            
            print("Kéo cửa sổ xuống")
            current_position = pyautogui.position()
            print(current_position)
            new_y = current_position.y + 400
            pyautogui.moveTo(current_position.x, new_y)
        
    else:
        # Không làm gì cả
        pass

# Tạo trình theo dõi sự kiện chuột

mouse_listener = pynput.mouse.Listener(on_click=on_click)

# Bắt đầu lắng nghe sự kiện chuột
mouse_listener.start()

# Giữ chương trình chạy cho đến khi bị thoát
mouse_listener.join()
#4db609a5019f1b092c489d61b9f4f295
#79564b1dfd2499820b6c46457da8e008
#4509d23beed669e55681842c9cdc9fd1
#b7534ce15e8278b8a857c093541fa735
#0b055314b175a4a0c7c4dcb7255ba47f
#1892319b19e3143de87c71834c162043
#5ae1f6367d1ae4a4a4dc23e9c1e07f0b
#7c515898778d00a5f6c83a0cbb7160bd