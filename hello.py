def main():
    print("Hello from internship!")
    dict_1 = {
        "sfdfff": "vejrovjreo",
        "sdffdf": "veejovjreo",
        "sfdfff": "veejrovjeo",
        "sfdfdf": "veejreo",
    }
    print(dict_1)


def binary_search(nums, target):
    l, r = 0, len(nums) - 1

    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] < target:
            l = mid + 1
        elif nums[mid] > target:
            r = mid - 1
        else:
            return mid
    return -1


if __name__ == "__main__":
    main()
    print(binary_search(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], target=2))
