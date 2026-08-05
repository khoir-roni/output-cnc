import os
import re
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_gcode_files():
    # Get all .nc, .ngc, .gcode files in current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith(('.nc', '.ngc', '.gcode'))]
    return sorted(files)

def fix_line(line, plunge_speed, simplify_m3, use_m2):
    # Gcode comments are in parentheses () or after semicolon ;
    comment = ""
    comment_idx = -1
    for char_idx, char in enumerate(line):
        if char == ';' or char == '(':
            comment_idx = char_idx
            break
            
    if comment_idx != -1:
        comment = line[comment_idx:]
        code_part = line[:comment_idx].strip()
    else:
        code_part = line.strip()

    if not code_part:
        return line, False, False, False, False, False

    # Stats tracking helpers
    m3_fixed = False
    m30_fixed = False
    plunge_fixed = False
    g0_g00_fixed = False
    g1_g01_fixed = False

    # Strip M3 and S parameters if simplifying spindle
    if simplify_m3:
        # Strip M3, M03 commands (with or without trailing speed parameter S)
        new_code = re.sub(r'\bM0?3\s*(S\s*\d+(\.\d+)?)?\b', '', code_part, flags=re.IGNORECASE)
        new_code = re.sub(r'\bM0?3S\s*\d+(\.\d+)?\b', '', new_code, flags=re.IGNORECASE)
        # Strip any standalone S speed parameters
        new_code = re.sub(r'\bS\s*\d+(\.\d+)?\b', '', new_code, flags=re.IGNORECASE)
        new_code = new_code.strip()
        if new_code != code_part:
            code_part = new_code
            m3_fixed = True

    # Replace M30 with M2
    if use_m2:
        new_code = re.sub(r'\bM30\b', 'M2', code_part, flags=re.IGNORECASE)
        if new_code != code_part:
            code_part = new_code
            m30_fixed = True

    # Check for G0/G00/G1/G01
    has_g0 = bool(re.search(r'\bG00?\b', code_part, re.IGNORECASE))
    has_g1 = bool(re.search(r'\bG01?\b', code_part, re.IGNORECASE))

    if has_g0:
        # Check if Z is plunging down (contains Z-)
        is_plunge = bool(re.search(r'Z\s*-\s*\d', code_part, re.IGNORECASE))
        if is_plunge:
            # Change G0/G00 to G01
            code_part = re.sub(r'\bG00?\b', 'G01', code_part, flags=re.IGNORECASE)
            # Add or update feedrate
            if re.search(r'F\s*\d', code_part, re.IGNORECASE):
                code_part = re.sub(r'F\s*\d+(\.\d+)?', f'F{plunge_speed}', code_part, flags=re.IGNORECASE)
            else:
                code_part = f"{code_part} F{plunge_speed}"
            plunge_fixed = True
        else:
            # Standard rapid move, change G0 to G00
            code_part = re.sub(r'\bG00?\b', 'G00', code_part, flags=re.IGNORECASE)
            # Remove feedrate F since rapid runs at max machine speed
            code_part = re.sub(r'\s*F\s*\d+(\.\d+)?', '', code_part, flags=re.IGNORECASE)
            g0_g00_fixed = True
            
    elif has_g1:
        # Change G1 to G01
        new_code = re.sub(r'\bG1\b', 'G01', code_part, flags=re.IGNORECASE)
        if new_code != code_part:
            code_part = new_code
            g1_g01_fixed = True

    # Reconstruct the line
    fixed_line = code_part
    if comment:
        fixed_line = f"{fixed_line} {comment}" if fixed_line else comment
        
    return fixed_line, m3_fixed, m30_fixed, plunge_fixed, g0_g00_fixed, g1_g01_fixed

def main():
    clear_screen()
    print("=" * 60)
    print("        CNC G-Code Converter & Fixer Utility")
    print("        Created by Antigravity AI")
    print("=" * 60)
    print()

    # Step 1: Select Input File
    files = get_gcode_files()
    # Remove fix_gcode.py from list
    files = [f for f in files if f != 'fix_gcode.py']
    
    input_file = ""
    if files:
        print("File G-Code yang ditemukan di direktori saat ini:")
        for idx, f in enumerate(files, 1):
            print(f"  [{idx}] {f}")
        print("  [0] Masukkan path file secara manual")
        print()
        
        while True:
            try:
                choice = input("Pilih file (angka) atau masukkan '0': ").strip()
                if choice == '0':
                    break
                idx = int(choice)
                if 1 <= idx <= len(files):
                    input_file = files[idx - 1]
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
            except ValueError:
                print("Masukkan angka yang valid.")
    
    if not input_file:
        while True:
            input_file = input("Masukkan path file G-code asal (contoh: C:\\path\\ke\\file.nc): ").strip().strip('"\'')
            if os.path.isfile(input_file):
                break
            print("File tidak ditemukan! Periksa kembali path file Anda.")

    # Step 2: Determine Output File
    default_output = os.path.splitext(input_file)[0] + "_fixed" + os.path.splitext(input_file)[1]
    if default_output.endswith('.nc'):
        default_output = default_output[:-3] + '.ngc' # Prefer .ngc as it's the working extension
    
    print(f"\nDefault file output: {default_output}")
    output_file = input(f"Masukkan nama file output [Tekan Enter untuk default]: ").strip().strip('"\'')
    if not output_file:
        output_file = default_output

    # Step 3: Interactive Configuration
    print("\n" + "-" * 40)
    print("Konfigurasi Konversi:")
    print("-" * 40)
    
    # 3.1 Plunge speed
    plunge_speed = 250
    val = input(f"Batas Kecepatan Turun Z (Plunge Feedrate) [Default: {plunge_speed} mm/min]: ").strip()
    if val:
        try:
            plunge_speed = float(val)
        except ValueError:
            print(f"Nilai tidak valid, menggunakan default: {plunge_speed}")

    # 3.2 Spindle speed
    remove_s = input("Pindahkan M3 ke Header & Hapus Kecepatan S dari Body (seperti I O gra_0001.ngc)? [Y/n]: ").strip().lower()
    if remove_s not in ('n', 'no'):
        simplify_m3 = True
    else:
        simplify_m3 = False

    # 3.3 End of file
    eof_cmd = input("Gunakan perintah penutup M2 (seperti file yang berfungsi) dibanding M30? [Y/n]: ").strip().lower()
    if eof_cmd not in ('n', 'no'):
        use_m2 = True
    else:
        use_m2 = False

    # Step 4: Process File
    print("\nMemulai proses konversi...")
    
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            
        # Clean trailing commands from input lines to make room for our custom footer
        # We will strip trailing M30, M2, M5, M05, % and empty lines.
        # We will also strip the final Z-retract move, because we will replace it with G00 Z5.000000.
        while lines:
            last_line = lines[-1].strip().upper()
            if not last_line:
                lines.pop()
                continue
            if last_line in ('M30', 'M2', 'M5', 'M05', '%'):
                lines.pop()
                continue
            # Check for trailing retract: G0/G1 move with Z and no Z-
            if (last_line.startswith('G0 ') or last_line.startswith('G00 ') or last_line.startswith('G1 ') or last_line.startswith('G01 ')) and 'Z' in last_line and 'Z-' not in last_line:
                lines.pop()
                continue
            break

        out_lines = []
        out_lines.append('%\n')
        out_lines.append('(Header)\n')
        out_lines.append(f'(Fixed: {os.path.basename(input_file)} -> {os.path.basename(output_file)})\n')
        out_lines.append('(Generated & Repaired by Antigravity G-Code Fixer)\n')
        if simplify_m3:
            out_lines.append('M3\n')
        out_lines.append('(Header end.)\n')
        
        stat_g0_g00 = 0
        stat_g1_g01 = 0
        stat_plunge_fixed = 0
        stat_m3_fixed = 0
        stat_m30_fixed = 0
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
                
            fixed_line, m3_f, m30_f, plunge_f, g0_g00_f, g1_g01_f = fix_line(
                line_str, plunge_speed, simplify_m3, use_m2
            )
            
            if m3_f: stat_m3_fixed += 1
            if m30_f: stat_m30_fixed += 1
            if plunge_f: stat_plunge_fixed += 1
            if g0_g00_f: stat_g0_g00 += 1
            if g1_g01_f: stat_g1_g01 += 1
            
            if fixed_line.strip():
                out_lines.append(fixed_line + '\n')
            
        # Append the custom Z-up, spindle stop, and XY home footer
        out_lines.append('G00 Z5.000000\n\n')
        out_lines.append('(Footer)\n')
        out_lines.append('M5\n')
        out_lines.append('G00 X0.0000 Y0.0000\n')
        out_lines.append('M2\n')
        out_lines.append('(Using default footer. To add your own footer create file "footer" in the output dir.)\n')
        out_lines.append('(end)\n')
        out_lines.append('%')
        
        with open(output_file, 'w') as f:
            f.writelines(out_lines)
            
        print("\n" + "=" * 60)
        print("          PROSES KONVERSI SELESAI DENGAN SUKSES!")
        print("=" * 60)
        print(f"File Output disimpan di: {os.path.abspath(output_file)}")
        print("\nStatistik Perbaikan:")
        print(f"  - Perintah G0/G00 diubah (rapid travel)  : {stat_g0_g00}")
        print(f"  - Perintah G1 diubah ke G01              : {stat_g1_g01}")
        print(f"  - Plunge Rapid (Z-) diubah ke G01 (feed) : {stat_plunge_fixed}")
        print(f"  - Perintah M3 dipindah ke header & body disederhanakan: {stat_m3_fixed}")
        print(f"  - Perintah penutup M30 diubah ke M2      : {stat_m30_fixed}")
        print("-" * 60)
        print("Silakan muat file baru tersebut ke mesin CNC Anda!")
        
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan saat memproses file: {e}")
        
    input("\nTekan Enter untuk keluar...")

if __name__ == '__main__':
    main()
