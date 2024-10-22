import os

def split_file(file_name, piece_size, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(file_name, 'rb') as file:
        i = 0
        while True:
            piece = file.read(piece_size)
            if not piece:
                break
            with open(f'{output_dir}/piece_{i}.dat', 'wb') as piece_file:
                piece_file.write(piece)
            i += 1
    print(f"File split into {i} pieces")

def merge_file(pieces, output_file):
    with open(output_file, 'wb') as output:
        for piece in pieces:
            with open(piece, 'rb') as piece_file:
                output.write(piece_file.read())
    print(f"File merged into {output_file}")
