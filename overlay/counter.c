#include <gtk/gtk.h>
#include <gdk/gdkscreen.h>
#include <cairo.h>

static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer user_data);

static int x = 0;
static int y = 0;
static char str[4];
#define IMAGE_WIDTH 200
#define IMAGE_HEIGHT 200

int main(int argc, char **argv)
{
    gtk_init(&argc, &argv);
    if (argc != 2)
        return 0;
    strncpy(str, argv[1], 4);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_POPUP);
    GdkScreen *screen = gtk_widget_get_screen(window);
    int w = gdk_screen_width();
    int h = gdk_screen_height();

    gtk_widget_set_app_paintable(window, TRUE);

    g_signal_connect(G_OBJECT(window), "expose-event", G_CALLBACK(expose), NULL);

    GdkColormap *colormap = gdk_screen_get_rgba_colormap(screen);
    gtk_widget_set_colormap(window, colormap);

    gtk_window_present(GTK_WINDOW(window));

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}

static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer userdata)
{
    cairo_t *cr = gdk_cairo_create(widget->window);
    cairo_set_operator(cr, CAIRO_OPERATOR_SOURCE);

    gtk_window_resize(GTK_WINDOW(widget), 130, 80);
    gtk_window_move(GTK_WINDOW(widget), x, y);
    printf(str);

    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_paint(cr);
    cairo_select_font_face(cr, "monospace", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_NORMAL);
    cairo_set_font_size(cr, 60);
    cairo_set_source_rgb(cr, 0, 0, 0);
    cairo_move_to(cr, 10, 60);
    cairo_show_text(cr, str);

    cairo_destroy(cr);
    return FALSE;
}