#include <X11/Xlib.h>
#include <X11/Xutil.h>

int main()
{

    Display *dpy = XOpenDisplay(NULL);

    int whiteColor = WhitePixel(dpy, DefaultScreen(dpy));

    XVisualInfo vinfo;
    XMatchVisualInfo(dpy, DefaultScreen(dpy), 32, TrueColor, &vinfo);
    XSetWindowAttributes attributes;
    attributes.colormap = XCreateColormap(dpy, DefaultRootWindow(dpy), vinfo.visual, AllocNone);
    attributes.border_pixel = 0;
    attributes.background_pixel = 0;
    attributes.override_redirect = true;
    unsigned long attrMask = CWBorderPixel | CWBackPixel | CWOverrideRedirect | CWColormap;

    Window w = XCreateWindow(dpy, DefaultRootWindow(dpy), 0, 0, 200, 100, 0, vinfo.depth, InputOutput, vinfo.visual, attrMask, &attributes);

    XSelectInput(dpy, w, StructureNotifyMask);
    XMapWindow(dpy, w);

    GC gc = XCreateGC(dpy, w, 0, NULL);
    XSetForeground(dpy, gc, whiteColor);
    XSetLineAttributes(dpy, gc, 20, LineSolid, CapNotLast, JoinMiter);

    for (;;)
    {
        XEvent e;
        XNextEvent(dpy, &e);
        if (e.type == MapNotify)
            break;
    }
    XDrawLine(dpy, w, gc, 10, 60, 180, 20);

    XFlush(dpy);
    while(1);
}
