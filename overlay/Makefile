SRC := $(wildcard *.cpp)
OBJ := $(SRC:%.cpp=%.o)

CPPFLAGS := -MMD -MP
CFLAGS   := -Wall `pkg-config --cflags freetype2`
LDFLAGS  :=

# TODO: remove libs that are notneeded
LDLIBS   := -lX11 -lXext -lXfixes -lXrandr -lXft -lfreetype

.PHONY: all clean

all: overlay

overlay: $(OBJ)
	$(CXX) $(LDFLAGS) $^ $(LDLIBS) -o $@

%.o: %.cpp
	$(CXX) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

clean:
	@$(RM) -r overlay *.o *.d
