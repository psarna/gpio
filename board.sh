#!/bin/bash

BOUNCE_PERIOD=0.05
TIMER_PERIOD=0.07

declare -A used
pids=()

hits=0
timer_count=10

function mpc_toggle() {
	if mpc | grep playing &> /dev/null; then
		echo "stopping"
		mpc stop &> /dev/null
	else
		echo "playing"
		mpc play &> /dev/null
	fi
}

function timer_function() {
	case $hits in
	1) mpc_toggle
	;;
	2) mpc next
	;;
	3) mpc volume -5
	;;
	4) mpc volume +5
	;;
	*) echo "too many claps"
	;;
	esac
}

function tactile_action() {
	mpc_toggle
}

function tactile2_action() {
	mpc next &> /dev/null
}

function noise_action() {
	kill -USR1 $$ 
}

function init_dev() {
	local device=$1
	local devnum=$2
	local updown=${3:-up}
	eval $device=$devnum
	used[$device]=0
	gpio -g mode $devnum 'in'
	gpio -g mode $devnum $updown
}

function serve_dev() {
	local device=$1
	local period=${2:-$BOUNCE_PERIOD}
	local event=${3:-falling}
	local devnum=${!device}
	while true; do
		gpio -g wfi $devnum $event
		${device}_action
		sleep $period
	done
}

function close_outerr() {
	exec 1<&-
	exec 2<&-
	
	exec 1<>/dev/null
	exec 2>&1
}

function main() {
	close_outerr
	init_dev tactile 21
	init_dev tactile2 12
	init_dev noise 4

	serve_dev tactile 0.2 &
	pids+=($!)
	serve_dev tactile2 0.2 &
	pids+=($!)
	serve_dev noise &
	pids+=($!)

	trap 'pkill board.sh' SIGINT
	trap 'timer_count=10; hits=$((hits+1))' SIGUSR1

	while true; do
		wait
		while [ $timer_count -gt 0 ]; do
			sleep $TIMER_PERIOD
			timer_count=$((timer_count-1))
		done
		timer_function $hits
		hits=0
	done
}

main
