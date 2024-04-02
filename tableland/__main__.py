if __name__ == "__main__":
    try:
        print("test")

    except RuntimeError as e:
        print(f"Error occurred during runtime: {e}")
        exit(1)
