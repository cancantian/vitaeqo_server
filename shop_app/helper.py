def handle_uploaded_file(input_file, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in input_file.chunks():
            destination.write(chunk)