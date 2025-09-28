class Cinema:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_hall(self, room):
        self.rooms.append(room)

    def get_nearest_session(self, title):
        nearest = None
        for room in self.rooms:
            show = room.get_nearest_session(title)
            if show and (not nearest or show.time < nearest.time):
                nearest = show
        return nearest

    def find_seats_together(self, count):
        for room in self.rooms:
            for show in room.shows:
                if show.has_adjacent_seats(count):
                    return show
        return None


class Hall:
    def __init__(self, name, seats):
        self.name = name
        self.capacity = seats
        self.shows = []

    def add_session(self, show):
        self.shows.append(show)
        show.hall_name = self.name

    def get_nearest_session(self, title):
        nearest = None
        for show in self.shows:
            if show.title == title and (not nearest or show.time < nearest.time):
                nearest = show
        return nearest


class Session:
    def __init__(self, title, length, time):
        self.title = title
        self.length = length
        self.time = time
        self.seats = {}
        self.hall_name = None
        self.sold_seats = set()

    def set_seat_configuration(self, config):
        self.seats = config

    def sell_tickets(self, count):
        available = self.get_available_list()
        if count <= len(available):
            for i in range(count):
                self.sold_seats.add(available[i])
            return True
        return False

    def get_available_list(self):
        available_list = []
        for row, seats_count in self.seats.items():
            for seat_num in range(1, seats_count + 1):
                seat_id = f"{row}{seat_num}"
                if seat_id not in self.sold_seats:
                    available_list.append(seat_id)
        return available_list

    def has_adjacent_seats(self, count):
        available = self.get_available_list()
        row_seats = {}

        for seat in available:
            row = seat[0]
            num = int(seat[1:])
            if row not in row_seats:
                row_seats[row] = []
            row_seats[row].append(num)

        for row, numbers in row_seats.items():
            numbers.sort()
            for i in range(len(numbers) - count + 1):
                if all(numbers[i + j] == numbers[i] + j for j in range(count)):
                    return True
        return False

    def print_seat_map(self):
        print(f"\nПлан зала '{self.title}':")
        for row, total in self.seats.items():
            line = f"Ряд {row}: "
            for seat_num in range(1, total + 1):
                seat_id = f"{row}{seat_num}"
                if seat_id in self.sold_seats:
                    line += "[X] "
                else:
                    line += "[ ] "
            print(line)


# Пример входных данных
cinema = Cinema("Киномир")

room1 = Hall("Зал 1", 50)
room2 = Hall("Зал 2", 40)

show1 = Session("Аватар", 120, "2023-11-02 16:00")
show1.set_seat_configuration({"A": 8, "B": 8, "C": 8, "D": 12})

show2 = Session("Один дома", 90, "2023-11-02 18:30")
show2.set_seat_configuration({"A": 6, "B": 8, "C": 8, "D": 10})

room1.add_session(show1)
room2.add_session(show2)

cinema.add_hall(room1)
cinema.add_hall(room2)

tickets = 2
if show1.sell_tickets(tickets):
    print(f"Продано {tickets} билета на '{show1.title}'")
else:
    print(f"Нет мест на '{show1.title}'")

film = "Аватар"
nearest = cinema.get_nearest_session(film)
if nearest:
    print(f"\nБлижайший сеанс '{film}':")
    print(f"Кинотеатр: {cinema.name}")
    print(f"Зал: {nearest.hall_name}")
    print(f"Время: {nearest.time}")
else:
    print(f"Фильм '{film}' не найден")

together = 3
found_show = cinema.find_seats_together(together)
if found_show:
    print(f"\nНайден сеанс с {together} местами рядом:")
    print(f"Фильм: {found_show.title}")
    print(f"Зал: {found_show.hall_name}")
    print(f"Время: {found_show.time}")
else:
    print(f"\nНет сеансов с {together} местами рядом")

show1.print_seat_map()

print(f"\nДоступно мест на 'Аватар': {len(show1.get_available_list())}")
print(f"Есть 3 места рядом: {show1.has_adjacent_seats(3)}")
