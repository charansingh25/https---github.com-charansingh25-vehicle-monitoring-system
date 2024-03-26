# CFLAGS=-Wall -Wextra -g
# LDLIBS=

# SRCS=top_proc.c example.c
# SRCS2=func_first.c
# SRCS3=func_second.c


# OBJS=$(subst .c,.o,$(SRCS))
# OBJS2=$(subst .c,.exe, $(SRCS2))
# OBJS3=$(subst .c,.exe, $(SRCS3))


# EXAMPLE= new_example
# EXAMPLE2 = first
# EXAMPLE3 = second



# SLEEP_TIME = 10

# $(EXAMLPE2): $(OBJS)
# 	$(CC) $(CFLAGS) $(LDLIBS) $(OBJS) -o $(EXAMLPE2)

first :
	python3 serialcomm.py

second :
	python3 model.py


# all: $(EXAMPLE) execute run_app $(EXAMPLE2) $(EXAMPLE3) first_execute

# $(EXAMPLE): $(OBJS)
# 	$(CC) $(CFLAGS) $(LDLIBS) $(OBJS) -o $(EXAMPLE)

# execute:
# 	./new_example

# run_app:
# 	python3 app_new.py

# $(EXAMPLE2) : 
# 	gcc $(SRCS2) -o $(EXAMPLE2)


# $(EXAMPLE3) : 
# 	gcc $(SRCS3) -o $(EXAMPLE3)

# first_execute: $(EXAMPLE2) $(EXAMPLE3)
# 	while true; do ./$(EXAMPLE2); ./$(EXAMPLE3); python3 popup.py; make SLEEPER; done

# run_popup:
# 	python3 popup.py

# SLEEPER: 
# 	sleep $(SLEEP_TIME)


# .PHONY: clean

# clean:
# 	rm -f $(OBJS) $(EXAMPLE)
# 	rm -f $(OBJS2) $(EXAMPLE2)
# 	rm -f $(OBJS3) $(EXAMPLE3)