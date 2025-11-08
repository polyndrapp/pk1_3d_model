import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.image import imread

# === КООРДИНАТЫ ===
A = (60, 130)
A_ = (56, 133)
B = (100, 50)
B_ = (100, 45)
C = (140, 130)
C_ = (144, 133)
O = (100, 100)

# === ПАРАМЕТРЫ ОКРУЖНОСТЕЙ ===
r = 20
r_ = 17
R = 90

# === ФУНКЦИЯ ПОВОРОТА НА 180° ВОКРУГ ЦЕНТРА ===
def rotate_180(points, center=(100, 100)):
    cx, cy = center
    rotated = []
    for x, y in points:
        x_new = 2 * cx - x
        y_new = 2 * cy - y
        rotated.append((x_new, y_new))
    return rotated

# Поворачиваем все вершины на 180°
A, B, C, A_, B_, C_ = rotate_180([A, B, C, A_, B_, C_])


# === СОЗДАЁМ ФИГУРУ ===
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.set_xlim(0, 200)
ax.set_ylim(0, 200)
ax.axis('off')

# === ДОБАВЛЕНИЕ КАРТИНКИ В ТРЕУГОЛЬНИК ===
image_path = r"D:\своя игра\photo_2025-10-27_23-26-15.jpg"
try:
    img = imread(image_path)
    triangle = Polygon([A, B, C], closed=True, facecolor='white', edgecolor='none', zorder=2.5)
    ax.add_patch(triangle)  # белый фон треугольника — закрывает всё под ним

    ax.imshow(
        img,
        extent=[0, 200, 0, 200],
        clip_path=triangle,
        clip_on=True,
        zorder=3
    )
except FileNotFoundError:
    print(f"⚠️ Картинка '{image_path}' не найдена, фон треугольника пропущен.")

# === ОТРИСОВКА ТРЕУГОЛЬНИКОВ ===
def draw_triangle(points, **kwargs):
    x, y = zip(*points)
    x += (x[0],)
    y += (y[0],)
    ax.plot(x, y, **kwargs)

# Основной треугольник
draw_triangle([A, B, C], color='black', linewidth=2)

# Пунктирный треугольник
dash_pattern = (0, (6, 5))
draw_triangle([A_, B_, C_], color='black', linestyle=dash_pattern, linewidth=1.5)

# === МАЛЫЙ КРУГ (пунктир из 30° секторов) с белым фоном ===
circle_small_bg = plt.Circle(O, r_, color='white', zorder=2.7)  # белый фон поверх линии, под треугольником
ax.add_artist(circle_small_bg)

for angle in np.arange(0, 360, 60):
    theta = np.radians(np.linspace(angle, angle + 30, 100))
    x_small = O[0] + r_ * np.cos(theta)
    y_small = O[1] + r_ * np.sin(theta)
    ax.plot(x_small, y_small, color='black', linewidth=1.2, zorder=3.2)

# === БОЛЬШОЙ КРУГ (сплошной) ===
circle_outer_bg = plt.Circle(O, r, color='white', zorder=2.7)
ax.add_artist(circle_outer_bg)

# добавляем белую заливку внутрь круга
circle_inner_fill = plt.Circle(O, r, color='white', zorder=3.1)
ax.add_artist(circle_inner_fill)

# контур круга
circle_outer = plt.Circle(O, r, color='black', fill=False, linewidth=1.5, zorder=3.2)
ax.add_artist(circle_outer)



# === БОЛЬШАЯ ДУГА (снизу) ===
theta = np.linspace(-np.pi / 6, np.pi, 200)
x_arc = O[0] + R * np.cos(theta + np.pi)
y_arc = O[1] + R * np.sin(theta + np.pi)
ax.plot(x_arc, y_arc, color='black', linewidth=1.5, zorder=4)

# === ОСЬ XY (рисуется ПОД фигурой) ===
start = np.array([0, 140])
end = np.array([200, 97])

# линия XY под всем
ax.plot([start[0], end[0]], [start[1], end[1]], color='black', linewidth=1, zorder=0)

# стрелка и подписи
arrow_length = 6
arrow_angle = np.deg2rad(20)

# вычисляем направление стрелки
dx, dy = end - start
angle = np.arctan2(dy, dx)

# рисуем стрелку вручную (чтобы zorder сработал)
arrow_x = [
    end[0],
    end[0] - arrow_length * np.cos(angle - arrow_angle),
    end[0] - arrow_length * np.cos(angle + arrow_angle),
    end[0]
]
arrow_y = [
    end[1],
    end[1] - arrow_length * np.sin(angle - arrow_angle),
    end[1] - arrow_length * np.sin(angle + arrow_angle),
    end[1]
]
ax.fill(arrow_x, arrow_y, color='black', zorder=0)

# подписи
ax.text(end[0] + 3, end[1], 'Y', fontsize=10, zorder=0)
ax.text(start[0] - 5, start[1], 'X', fontsize=10, zorder=0)




# === БЕЛЫЙ ФОН ===
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

plt.show()