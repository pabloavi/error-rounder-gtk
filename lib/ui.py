def css():
    return r"""
    .section-title{
        font-size: large;
        font-weight: bold;
    }
    """


def ui():
    return r"""<?xml version='1.0' encoding='UTF-8'?>
<!-- Created with Cambalache 0.12.1 -->
<interface>
  <!-- interface-name error-rounder.ui -->
  <requires lib="gtk" version="4.10"/>
  <requires lib="libadwaita" version="1.3"/>
  <object class="AdwApplicationWindow" id="main_window">
    <property name="default-height">800</property>
    <property name="default-width">1200</property>
    <child>
      <object class="GtkBox" id="main_box">
        <property name="margin-bottom">20</property>
        <property name="margin-end">20</property>
        <property name="margin-start">20</property>
        <property name="margin-top">20</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkBox" id="options_label_box">
            <property name="margin-bottom">10</property>
            <property name="margin-top">10</property>
            <child>
              <object class="GtkLabel" id="options_label">
                <property name="css-classes">section-title</property>
                <property name="label">Opciones</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkBox" id="options_hbox">
            <property name="orientation">vertical</property>
            <property name="spacing">10</property>
            <child>
              <object class="GtkBox" id="auto_update_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Actualizar automáticamente la salida</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSwitch" id="auto_update_switch">
                    <property name="active">True</property>
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkBox" id="error_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Usar un error específico para todas las entradas</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSwitch" id="force_error_switch">
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                  </object>
                </child>
                <child>
                  <object class="GtkEntry" id="error_entry">
                    <property name="input-purpose">number</property>
                    <property name="placeholder-text">0.10</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkBox" id="switch_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Usar solo primera y última columnas</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSwitch" id="first_and_last_columns_only_switch">
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkBox">
                <property name="spacing">10</property>
                <child>
                  <object class="GtkBox">
                    <property name="orientation">vertical</property>
                    <property name="spacing">5</property>
                    <property name="visible">False</property>
                    <child>
                      <object class="GtkLabel">
                        <property name="label">Formato de cada valor</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkComboBoxText" id="rounded_format_combobox">
                        <property name="halign">center</property>
                        <property name="hexpand">True</property>
                      </object>
                    </child>
                  </object>
                </child>
                <child>
                  <object class="GtkBox">
                    <property name="orientation">vertical</property>
                    <property name="spacing">5</property>
                    <property name="visible">False</property>
                    <child>
                      <object class="GtkLabel">
                        <property name="label">Formato de impresión</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkComboBoxText" id="print_format_combobox">
                        <property name="halign">center</property>
                        <property name="hexpand">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkBox" id="format_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Formato</property>
                  </object>
                </child>
                <child>
                  <object class="GtkComboBoxText" id="format0_combobox">
                    <property name="halign">center</property>
                    <property name="hexpand">True</property>
                  </object>
                </child>
                <child>
                  <object class="GtkComboBoxText" id="format1_combobox">
                    <property name="halign">center</property>
                    <property name="hexpand">True</property>
                  </object>
                </child>
                <child>
                  <object class="GtkComboBoxText" id="format2_combobox">
                    <property name="halign">center</property>
                    <property name="hexpand">True</property>
                  </object>
                </child>
                <child>
                  <object class="GtkEntry" id="hybrid_entry">
                    <property name="input-purpose">number</property>
                    <property name="placeholder-text">0.10</property>
                    <property name="sensitive">False</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkBox" id="multi_error_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Error de cada columna</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSwitch" id="per_column_error_switch">
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                  </object>
                </child>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="margin-bottom">20</property>
            <property name="margin-top">20</property>
            <property name="orientation">vertical</property>
          </object>
        </child>
        <child>
          <object class="GtkBox" id="input_label_box">
            <child>
              <object class="GtkLabel" id="input_label">
                <property name="css-classes">section-title</property>
                <property name="label">Entrada</property>
                <property name="margin-bottom">10</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkBox" id="input_box">
            <property name="orientation">vertical</property>
            <property name="spacing">10</property>
            <child>
              <object class="GtkBox" id="custom_input_switch_box">
                <property name="spacing">20</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label">Usar una entrada personalizada</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSwitch" id="custom_input_switch">
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkScrolledWindow" id="input_scrolled_window">
                <property name="vexpand">True</property>
                <property name="visible">False</property>
                <child>
                  <object class="GtkTextView" id="input_textview"/>
                </child>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="margin-bottom">20</property>
            <property name="margin-top">20</property>
            <property name="orientation">vertical</property>
          </object>
        </child>
        <child>
          <object class="GtkBox" id="output_label_box">
            <child>
              <object class="GtkLabel" id="output_label">
                <property name="css-classes">section-title</property>
                <property name="label">Salida</property>
                <property name="margin-bottom">10</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkBox" id="output_box">
            <property name="orientation">vertical</property>
            <property name="spacing">10</property>
            <child>
              <object class="GtkBox">
                <property name="spacing">10</property>
                <child>
                  <object class="GtkButton" id="execute_button">
                    <property name="hexpand">True</property>
                    <property name="label">Actualizar</property>
                  </object>
                </child>
                <child>
                  <object class="GtkButton" id="clipboard_button">
                    <property name="hexpand">True</property>
                    <property name="label">Copiar al portapapeles</property>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkScrolledWindow">
                <property name="vexpand">True</property>
                <child>
                  <object class="GtkTextView" id="textview"/>
                </child>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""
