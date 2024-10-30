import pygame, sys, random
#tạo hàm cho game
def draw_floor(): #hàm vẽ floor và tạo hiệu ứng lặp lại của floor
    screen.blit(floor, (floor_x_pos, 650)) #Thêm floor
    screen.blit(floor, (floor_x_pos + 432, 650)) #Thêm floor thứ 2


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # chọn ngẫu nhiên chiều cao ống dưới
    pipe_gap = 200  # Khoảng cách giữa ống trên và ống dưới
    total_height = 650  # Tổng chiều cao từ sàn trở lên

    bottom_pipe_height = random_pipe_pos
    top_pipe_height = total_height - bottom_pipe_height - pipe_gap

    bottom_pipe = pipe_surface.get_rect(midtop=(500, 650 - bottom_pipe_height))  # tạo ống dưới từ mặt sàn
    top_pipe = pipe_surface.get_rect(midbottom=(500, 650 - bottom_pipe_height - pipe_gap))  # tạo ống trên với khoảng cách

    return bottom_pipe, top_pipe
# def create_pipe(): // chỉ tạo thử ống dưới để tính điểm. Khi tạo ra ống dưới và ống trên thì bird đi qua sẽ lấy số điểm x2.
#     random_pipe_pos = random.choice(pipe_height)  # Chọn ngẫu nhiên chiều cao ống dưới
#     pipe_gap = 200  # Khoảng cách giữa ống trên và ống dưới
#     total_height = 650  # Tổng chiều cao từ sàn trở lên

#     bottom_pipe_height = random_pipe_pos

#     bottom_pipe = pipe_surface.get_rect(midtop=(500, 650 - bottom_pipe_height))  # Tạo ống dưới từ mặt sàn

#     print(f"Chiều cao của ống dưới: {bottom_pipe_height}")  # In ra chiều cao của ống dưới

#     return bottom_pipe 

def move_pipe(pipes): #di chuyển ống
    for pipe in pipes: #duyệt qua từng ống
        pipe.centerx -= 4 #di chuyển ống qua trái 5 đơn vị trục x
    return pipes
def draw_pipe(pipes): #vẽ ống
    for pipe in pipes:
        if pipe.bottom >= 600: #in ra ống dưới
            screen.blit(pipe_surface, pipe)
        else: #in ra ống trên và lật lại
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) #lật ống theo trục y
            screen.blit(flip_pipe, pipe)
# def check_collision(pipes): #kiểm tra va chạm
#     for pipe in pipes:
#         if bird_rect.colliderect(pipe): #va cham giữa bird và ống
#             print(f"Chạm ống: {pipe}")
#             hit_sound.play()
#             return False
#         if bird_rect.top <=-75 or bird_rect.bottom >= 650: #va chạm giữa bird và floor
#             print(f"Chạm floor: {bird_rect}")
#             return False
#
#         print(f"bird_rect.top: {bird_rect.top}, bird_rect.bottom: {bird_rect.bottom}")
#
#     return True
def check_collision(pipes):  # kiểm tra va chạm
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # va chạm giữa bird và ống
            print(f"Va chạm với ống: {pipe}")  # Thêm debug log
            hit_sound.play()
            return False
    if bird_rect.top <= -250 or bird_rect.bottom >= 800:  # va chạm với giới hạn trên/dưới
        print(f"Va chạm với sàn: {bird_rect}")  # Thêm debug log
        return False

    return True

def rotate_bird(bird1): #xoay bird
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)#tạo hiệu ứng xoay bird, bird_movement là góc xoay theo chiều chuyển động của bird, 1 là kích thước của ảnh
    return new_bird
def bird_amination(): #tạo hiệu ứng bird bay, chuyển động giữa 3 ảnh bird
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main_game': #khi game đang chạy
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255)) #tạo điểm số, int(score) để lấy số nguyên, str() để chuyển số nguyên sang chuỗi
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'main_over': #khi game over
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))  # tạo điểm số, int(score) để lấy số nguyên,f''(ép kiểu string bất kỳ biến nào) để chuyển số nguyên sang chuỗi,
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HighScore: {int(high_score)}', True, (255, 255, 255))  # tạo điểm số, int(score) để lấy số nguyên, str() để chuyển số nguyên sang chuỗi
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score): #cập nhật điểm số
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512) #tăng chất lượng âm thanh
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
#tạo biến cho game
gravity = 0.25 # trọng lực
bird_movement = 0 #di chuyển của bird
game_active = False  #game đang chạy, chuyển về False khi game over
score = 0
high_score = 0
# passed_pipe = False  # Khởi tạo biến passed_pipe



#Chén bg
bg = pygame.image.load('assests/background-night.png').convert() #thêm convert() để đổi file ảnh thành file nhẹ hơn load ảnh nhanh hơn
bg = pygame.transform.scale2x(bg) #Scale ảnh lên gấp đôi
#Chèn Sàn
floor = pygame.image.load('assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#Tạo bird
bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] #tạo list bird 0, 1, 2
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('assests/yellowbird-midflap.png').convert_alpha() #thêm convert_alpha() để đổi file ảnh thành file nhẹ hơn load ảnh nhanh hơn và mất cái nền màu đen
# bird = pygame.transform.scale2x(bird) #Scale ảnh lên gấp đôi
bird_rect = bird.get_rect(center=(100, 384))  #Tạo hình chữ nhật bao quanh bird
 #Tạo timer cho bird
birdflap = pygame.USEREVENT + 1 #+1 để tạo timer khác với timer khác, tránh trùng lặp event với timer tạo ống
pygame.time.set_timer(birdflap, 200) #tạo timer cho bird sau mỗi 200ms(0.2s)
#Tạo ống
pipe_surface = pygame.image.load('assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] #tạo list ống
#tạo timer cho ống
spawpipe = pygame.USEREVENT
pygame.time.set_timer(spawpipe, 2000) #tạo ống sau mỗi 1200ms(1.2s)
pipe_height = [50,100, 150,200,250, 300, 350,400] #tạo chiều cao ống
#Tạo màn hình end game
game_over_surface = pygame.transform.scale2x((pygame.image.load('assests/message.png').convert_alpha()))
game_over_rect = game_over_surface.get_rect(center=(216, 384))
#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
# pipe_heights = []
# passed_pipes = []

#while loop game
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active: #
                    # print("space")
                    bird_movement = 0
                    bird_movement = -8 #khi nhấn space bird sẽ bay lên theo trục y 1 khoảng -10
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear() #xóa list ống, tạo game mới
                    # pipe_heights.clear()  # Đặt lại danh sách chiều cao ống
                    # passed_pipes.clear()  # Đặt lại danh sách các ống đã được vượt qua

                    bird_rect.center = (100, 384)#đặt lại vị trí bird
                    bird_movement = 0 #đặt lại trọng lực
                    score = 0 #đặt lại điểm số

            if event.type == spawpipe: #tạo ống mới
                bottom_pipe = create_pipe()

                # print("pipe")
                pipe_list.extend(create_pipe())#tạo ống mới và thêm vào list ống
                # print(create_pipe)
                # pipe_heights.append(bottom_pipe.height)  # Lưu trữ chiều cao ngẫu nhiên của ống dưới

            if event.type == birdflap: #tạo hiệu ứng bird bay
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_rect = bird_amination()

        screen.blit(bg, (0, 0)) #Thêm bg
        if game_active:
            #chim
            bird_movement += gravity #chim càng di chuyển thì trọng lực càng tăng
            bird_rect.centery += bird_movement #trọng lực bird theo trục y,
            rotated_bird = rotate_bird(bird) #xoay bird

            screen.blit(rotated_bird, bird_rect) #Thêm bird

            game_active = check_collision(pipe_list) #nếu không va chạm thì game vẫn chạy, ngược lại thì game over

            #ống
            pipe_list = move_pipe(pipe_list) #Lấy tất cả ống vừa đc tạo trong pipe_list và di chuyển rồi trả lại list ống mới
            draw_pipe(pipe_list)
            #Tăng điểm sau khi vượt qua ống
            # for pipe in pipe_list:
            #     if 95 < pipe.centerx < 105 and not passed_pipe:
            #         score += 1
            #         passed_pipe = True
            #     if pipe.centerx < 0:
            #         passed_pipe = False
            for pipe in pipe_list:
                if pipe.centerx == 100:
                     score += 0.5
                   
            score_display('main_game')
            # score_sound_countdown -= 1
            # if score_sound_countdown <= 0:
            #     score_sound.play()
            #     score_sound_countdown = 100
        else:
            score_display('main_over')
            high_score = update_score(score, high_score)
            screen.blit(game_over_surface, game_over_rect)
        #floor
        floor_x_pos -= 1 #di chuyển floor qua trái
        draw_floor()
        if floor_x_pos <= -432:#tạo hiệu ứng lặp lại của floor
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120 ) #tạo tốc độ chạy game là 120fps
except KeyboardInterrupt:
    print("Thoát game")
    pygame.quit()
    sys.exit()