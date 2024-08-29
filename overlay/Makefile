SRC := seal.c
OBJ := $(SRC:%.c=%.o)

SRC2 := counter.c
OBJ2 := $(SRC2:%.c=%.o)

CFLAGS=-Wall $$(pkg-config --cflags gtk+-2.0)
LDFLAGS := $$(pkg-config --libs gtk+-2.0)

.PHONY: all clean

all: halifaxseal halifaxcounter

halifaxseal: $(OBJ)
	$(CC) $(LDFLAGS) $^ -o $@


halifaxcounter: $(OBJ2)
	$(CC) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@$(RM) -r halifaxseal halifaxcounter *.o *.d
