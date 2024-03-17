from multiprocessing import Pool, cpu_count
import time

def factorize(num):
    divisors = [i for i in range(1, num + 1) if num % i == 0]
    return divisors

def factorize_parallel(numbers):
    num_cores = cpu_count()  # Отримуємо кількість ядер
    print(f"Number of CPU cores: {num_cores}")

    start_time = time.time()
    with Pool(num_cores) as pool:
        results = pool.map(factorize, numbers)
    end_time = time.time()

    print(f"Time taken (parallel): {end_time - start_time} seconds")
    return results

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    # Викликаємо функції factorize та factorize_parallel для кожного числа і зберігаємо результати
    start_time_sync = time.time()
    divisors_sync = [factorize(num) for num in numbers]
    end_time_sync = time.time()

    divisors_parallel = factorize_parallel(numbers)

    # Виводимо результати обчислень
    for num, divisors in zip(numbers, divisors_parallel):
        print(f"Divisors of {num} (parallel): {divisors}")

    for num, divisors in zip(numbers, divisors_sync):
        print(f"Divisors of {num} (synchronous): {divisors}")

    print(f"Time taken (synchronous): {end_time_sync - start_time_sync} seconds")
