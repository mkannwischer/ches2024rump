SRC := seal.c
OBJ := $(SRC:%.c=%.o)

CFLAGS=-Wall $$(pkg-config --cflags gtk+-2.0)
LDFLAGS := $$(pkg-config --libs gtk+-2.0)

.PHONY: all clean

all: halifaxseal

halifaxseal: $(OBJ)
	$(CC) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@$(RM) -r halifaxseal *.o *.d
