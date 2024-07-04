from camera import camera_function as cf

camera = cf.Camera()
camera.get_camera_source()
while True:
    camera.show_content()
    screen, filename = camera.make_screen()
    camera.screen_save(screen, filename)
    camera.turn_off_camera()




