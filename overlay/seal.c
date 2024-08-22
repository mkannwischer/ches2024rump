#include <gtk/gtk.h>
#include <gdk/gdkscreen.h>
#include <cairo.h>

#include <time.h>
#include <stdlib.h>

static gboolean expose(GtkWidget *widget, GdkEventExpose *event, gpointer user_data);

static int x = 0; 
static int y = 0;
#define IMAGE_WIDTH 200
#define IMAGE_HEIGHT 200

int main(int argc, char **argv)
{
    gtk_init(&argc, &argv);

    srand(time(NULL));

    GtkWidget *window = gtk_window_new(GTK_WINDOW_POPUP);
    GdkScreen *screen =  gtk_widget_get_screen(window);
    int w = gdk_screen_width();
    int h = gdk_screen_height();

    x = rand() % (w - IMAGE_WIDTH);
    y = rand() % (h - IMAGE_HEIGHT);

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
    cairo_set_operator (cr, CAIRO_OPERATOR_SOURCE);
    cairo_surface_t *img;
    int imgw, imgh;
    char *imgpath;
    imgpath = "seal.png";

    img = cairo_image_surface_create_from_png(imgpath);
    imgw = cairo_image_surface_get_width(img);
    imgh = cairo_image_surface_get_height(img);

    gtk_window_resize(GTK_WINDOW(widget), imgw, imgh);
    gtk_window_move(GTK_WINDOW(widget), x, y);
    
    cairo_set_source_surface(cr, img, 0, 0);
    cairo_paint (cr);
    cairo_destroy(cr);
    return FALSE;
}