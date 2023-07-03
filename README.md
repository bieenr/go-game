# AI bot - Cờ vây
## Cài đặt
Sử dụng anaconda
> conda create -n go-game

> conda activate go-game

> pip install -r requirements.txt

## Sử dụng
### AI vs AI
> python main.py --black [rand, greedy, ab, drop] --bdepth [depth for black] --bwidth [width for drop agent] --white [rand, greedy, ab, drop] --wdepth [depth for white] --wwidth [width for drop agent] --time-limit [giới hạn thời gian theo phút]

Trong đó
- rand: chiến thuật ngẫu nhiên
- greedy: chiến thuật tham lam
- ab: thuật toán cắt tỉa alpha-beta
- drop: thuật toán drop

### AI với người, thông qua GUI
> python menu_main.py

Agent mặc định là DropAgent với độ sâu 4, độ rộng 10.