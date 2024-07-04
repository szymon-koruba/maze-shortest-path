from camera import camera_function as cf

camera = cf.Camera()
camera.get_camera_source()
while True:
    camera.show_content()
    camera.make_screen()
    camera.turn_off_camera()




