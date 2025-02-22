'''
archivar v3.0 - migration from shell script to python script
extensive logging and error handling included
configuaration file: archivar_30.cfg includes directories, months, settings and regex
usage of ocrmypdf, pdftotext and rsync
rsync command is generated and executed can be dangerous, use with caution
normalization of slashes in directory paths to avoid rsync going wild in user's home directory
dryrun mode is available for testing
github: archivar_30
author: @mlp0911
date: 2025-02-22
'''

import os
import re
import configparser
from datetime import datetime
import subprocess
import logging

def setup_logger(log_dir, log_filename):
    """Set up the logger."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    console_handler = logging.StreamHandler()

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', handlers=[file_handler, console_handler])

def load_config(config_file):
    """Load the configuration file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"The configuration file '{config_file}' was not found.")
    
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config

def get_directories(config):
    """Get directories from the configuration file."""
    if 'directories' not in config:
        raise KeyError("The section 'directories' is missing in the configuration file")
    
    return (
        config['directories']['input_dir'],
        config['directories']['process_dir'],
        config['directories']['target_dir'],
        config['directories']['log_dir']
    )

def get_months(config):
    """Get months from the configuration file."""
    if 'months' not in config:
        raise KeyError("The section 'months' is missing in the configuration file")
    
    return {month: number for month, number in config['months'].items()}

def get_settings(config):
    """Get settings from the configuration file."""
    if 'settings' not in config:
        raise KeyError("The section 'settings' is missing in the configuration file")
    
    return config['settings']['mode'], config['settings'].getint('jobs')

def get_regex(config):
    """Get regex patterns from the configuration file."""
    if 'regex' not in config:
        raise KeyError("The section 'regex' is missing in the configuration file")
    
    return config['regex']['date_pattern']

def log(message, level=logging.INFO):
    """Log a message."""
    logging.log(level, message)

def normalize_slashes(text):
    """Normalize slashes in the text and ensure there is exactly one slash at the end."""
    text = re.sub(r'/+', '/', text)
    if not text.endswith('/'):
        text += '/'
    return text

def process_pdf(filepath, input_dir, process_dir, mode, jobs, date_pattern, months):
    """Process a PDF file."""
    log(f"Start processing {filepath} in {mode} mode")
    
    match = re.match(rf"{re.escape(input_dir)}(.*)\.pdf$", filepath)
    if not match:
        log(f"Pattern does not match file path: {filepath}", logging.WARNING)
        return
    
    dateiname = match.group(1)
    log(f"Filename: {dateiname}")
    
    match = re.match(
        rf"{re.escape(input_dir)}(.*)/(\d{{4}})(\d{{2}})(\d{{2}})_(\d{{6}})_(.*)_\d{{3}}(\d{{3}})\.(.*)",
        filepath
    )
    if match:
        kat1 = match.group(1)
        jahr = match.group(2)
        monat = match.group(3)
        tag = match.group(4)
        zeit = match.group(5)
        kat2 = match.group(6)
        lfdnr = match.group(7)
        ext = match.group(8)
        
        log(f"Extracted values - kat1: {kat1}, year: {jahr}, month: {monat}, day: {tag}, time: {zeit}, kat2: {kat2}, seqnum: {lfdnr}, ext: {ext}")
        
        neu = f"{jahr}{monat}{tag}{lfdnr}-{kat1}-{kat2}"
        
        output_dir = os.path.join(process_dir, kat1, kat2)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            log(f"Created directory: {output_dir}")
        
        output_pdf = os.path.join(output_dir, f"{neu}.pdf")
        ocrmypdf_cmd = ["ocrmypdf", "-j", str(jobs), "-l", "deu+eng", filepath, output_pdf]
        log(f"OCR command: {ocrmypdf_cmd}")
        if mode == 'hot':
            subprocess.run(ocrmypdf_cmd)
            log(f"OCR -> PDF: Done")
        else:
            log(f"Dryrun mode: OCR -> PDF: {ocrmypdf_cmd} (not executed)")
        
        datumdatei = f"{jahr}{monat}{tag}"
        datumtext = subprocess.run(
            ["pdftotext", "-l", "1", output_pdf, "-"],
            capture_output=True, text=True
        ).stdout
        datumtext = re.search(date_pattern, datumtext)
        if datumtext:
            datumtext = datumtext.group(0)
            log(f"Found date in text: {datumtext}")
            
            match = re.match(r"([0-9]{1,2})\.\s?([0-9]{1,2}|.*\s?)\.?([0-9]{2,4}$)", datumtext)
            if match:
                tagneu = match.group(1)
                monatneu = match.group(2)
                jahrneu = match.group(3)
                
                if re.match(r"^[0-9]{2}$", jahrneu):
                    jahrneu = f"20{jahrneu}"
                
                if not re.match(r"^[0-9]{2}$", monatneu):
                    monatneu = months.get(monatneu[:3], '01')
                datumneu = f"{jahrneu}{monatneu.zfill(2)}{tagneu.zfill(2)}"
                log(f"New date: {datumneu}")
                
                if re.match(r"^[0-9]{8}$", datumneu):
                    if datumneu != datumdatei:
                        dateinameneu = f"{datumneu}x{lfdnr}-{kat1}-{kat2}.pdf"
                    else:
                        dateinameneu = f"{datumneu}o{lfdnr}-{kat1}-{kat2}.pdf"
                else:
                    dateinameneu = f"{jahr}{monat}{tag}O{lfdnr}-{kat1}-{kat2}.pdf"
                
                if mode == 'hot':
                    log(f"Renaming file: {dateinameneu}")
                    os.rename(
                        output_pdf,
                        os.path.join(output_dir, f"{dateinameneu}")
                    )
                    log(f"Renamed file: {dateinameneu}")
                else:
                    log(f"Dryrun mode: Renamed file: {dateinameneu} (not executed)")
            else:
                log("Could not find or extract date in text", logging.WARNING)
        else:
            log("No date found in text", logging.WARNING)
    else:
        log(f"Match failed for file {filepath}", logging.WARNING)

def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_dir, 'archivar_30.cfg')
    
    config = load_config(config_file)
    input_dir, process_dir, target_dir, log_dir = get_directories(config)
    months = get_months(config)
    mode, jobs = get_settings(config)
    date_pattern = get_regex(config)
    
    log_filename = os.path.join(log_dir, f"archivar_30_{datetime.now().strftime('%Y-%m-%d')}.log")
    rsync_log_filename = os.path.join(log_dir, 'rsync_debug.log')
    setup_logger(log_dir, log_filename)
    
    log(f"<<<<<Script start: Mode {mode}>>>>>>", logging.INFO)
    
    # Normalize slashes in directories
    input_dir = normalize_slashes(input_dir)
    process_dir = normalize_slashes(process_dir)
    target_dir = normalize_slashes(target_dir)
    log_dir = normalize_slashes(log_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".pdf"):
                filepath = os.path.join(root, file)
                process_pdf(filepath, input_dir, process_dir, mode, jobs, date_pattern, months)
    
    log("Files are being moved and cleaned...", logging.INFO)
    
    # Normalize slashes again just before creating the rsync command
    normalized_process_dir = normalize_slashes(process_dir)
    normalized_target_dir = normalize_slashes(target_dir)
    
    # Prepare the rsync command
    rsync_cmd = [
        "rsync",
        "-avzh",
        "--remove-source-files",
        "--progress",
        f"--log-file={rsync_log_filename}",
        normalized_process_dir,
        normalized_target_dir
    ]
    
    if mode != 'hot':
        rsync_cmd.insert(2, '--dry-run')  # Add '--dry-run' option
    
    log(f"Generated rsync command: {' '.join(rsync_cmd)}")
    
    # Execute the rsync command
    rsync_result = subprocess.run(rsync_cmd, capture_output=True, text=True)
    log(f"rsync output: {rsync_result.stdout}")
    log(f"rsync error: {rsync_result.stderr}")
    
    if mode == 'hot':
        # Remove the original files from the input_dir only if mode is 'hot'
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".pdf"):
                    os.remove(os.path.join(root, file))
    else:
        log("Dryrun mode: Files were not moved or deleted", logging.INFO)
    
    log(f"<<<<<Script end: Mode {mode}>>>>>>", logging.INFO)

if __name__ == "__main__":
    main()
