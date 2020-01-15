#ifndef TRANSFORM_PLUGIN_GLOBAL_H
#define TRANSFORM_PLUGIN_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(TRANSFORM_PLUGIN_LIBRARY)
#  define TRANSFORM_PLUGINSHARED_EXPORT Q_DECL_EXPORT
#else
#  define TRANSFORM_PLUGINSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // TRANSFORM_PLUGIN_GLOBAL_H
