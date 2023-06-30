@REM extract time
python main.py --black ab --bdepth 3 --white ab --wdepth 4
python main.py --black ab --bdepth 2 --white ab --wdepth 1

python main.py --black greedy --bdepth 4 --white greedy --wdepth 3
python main.py --black greedy --bdpeth 2 --white greedy --wdepth 1

python main.py --black drop --bdepth 3 --bwidth 20 --white drop --wdepth 3 --wwwidth 15
python main.py --black drop --bdepth 3 --bwidth 10 --white drop --wdepth 3 --wwwidth 5

@REM compare every 2 bot
python main.py --black ab --bdepth 4 --white greedy --wdepth 4
python main.py --black ab --bdepth 4 --white greedy --wdepth 4
python main.py --black ab --bdepth 4 --white greedy --wdepth 4

python main.py --black greedy --bdepth 4 --white ab --wdepth 4
python main.py --black greedy --bdepth 4 --white ab --wdepth 4
python main.py --black greedy --bdepth 4 --white ab --wdepth 4



python main.py --black drop --bdepth 5 --bwidth 15 --white ab --wdepth 4
python main.py --black drop --bdepth 5 --bwidth 15 --white ab --wdepth 4
python main.py --black drop --bdepth 5 --bwidth 15 --white ab --wdepth 4

python main.py --black ab --bdepth 4 --white drop --wdepth 5 --wwwidth 15
python main.py --black ab --bdepth 4 --white drop --wdepth 5 --wwwidth 15
python main.py --black ab --bdepth 4 --white drop --wdepth 5 --wwwidth 15



python main.py --black drop --bdepth 5 --bwidth 15 --white greedy --wdepth 4
python main.py --black drop --bdepth 5 --bwidth 15 --white greedy --wdepth 4
python main.py --black drop --bdepth 5 --bwidth 15 --white greedy --wdepth 4

python main.py --black greedy --bdepth 4 --white drop --wdepth 5 --wwwidth 15
python main.py --black greedy --bdepth 4 --white drop --wdepth 5 --wwwidth 15
python main.py --black greedy --bdepth 4 --white drop --wdepth 5 --wwwidth 15


@REM time constraints?