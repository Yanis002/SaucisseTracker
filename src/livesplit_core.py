#!/usr/bin/env python3
# coding: utf-8

import sys, ctypes
from ctypes import c_char_p, c_void_p, c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64, c_size_t, c_ssize_t, c_float, c_double, c_bool, c_char, c_byte

# SaucisseTracker modification: fix the path to the library binaries
prefix = {'win32': ''}.get(sys.platform, 'lib')

extension = {'darwin': '.dylib', 'win32': '.dll'}.get(sys.platform, '.so')
livesplit_core_native = ctypes.cdll.LoadLibrary("lib/" + prefix + "livesplit_core" + extension)

livesplit_core_native.Analysis_calculate_sum_of_best.argtypes = (c_void_p, c_bool, c_bool, c_uint8, )
livesplit_core_native.Analysis_calculate_sum_of_best.restype = c_void_p
livesplit_core_native.Analysis_calculate_total_playtime_for_run.argtypes = (c_void_p, )
livesplit_core_native.Analysis_calculate_total_playtime_for_run.restype = c_void_p
livesplit_core_native.Analysis_calculate_total_playtime_for_timer.argtypes = (c_void_p, )
livesplit_core_native.Analysis_calculate_total_playtime_for_timer.restype = c_void_p
livesplit_core_native.AtomicDateTime_drop.argtypes = (c_void_p, )
livesplit_core_native.AtomicDateTime_drop.restype = None
livesplit_core_native.AtomicDateTime_is_synchronized.argtypes = (c_void_p, )
livesplit_core_native.AtomicDateTime_is_synchronized.restype = c_bool
livesplit_core_native.AtomicDateTime_to_rfc3339.argtypes = (c_void_p, )
livesplit_core_native.AtomicDateTime_to_rfc3339.restype = c_char_p
livesplit_core_native.Attempt_index.argtypes = (c_void_p, )
livesplit_core_native.Attempt_index.restype = c_int32
livesplit_core_native.Attempt_time.argtypes = (c_void_p, )
livesplit_core_native.Attempt_time.restype = c_void_p
livesplit_core_native.Attempt_pause_time.argtypes = (c_void_p, )
livesplit_core_native.Attempt_pause_time.restype = c_void_p
livesplit_core_native.Attempt_started.argtypes = (c_void_p, )
livesplit_core_native.Attempt_started.restype = c_void_p
livesplit_core_native.Attempt_ended.argtypes = (c_void_p, )
livesplit_core_native.Attempt_ended.restype = c_void_p
livesplit_core_native.AutoSplittingRuntime_new.argtypes = (c_void_p, )
livesplit_core_native.AutoSplittingRuntime_new.restype = c_void_p
livesplit_core_native.AutoSplittingRuntime_drop.argtypes = (c_void_p, )
livesplit_core_native.AutoSplittingRuntime_drop.restype = None
livesplit_core_native.AutoSplittingRuntime_load_script.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.AutoSplittingRuntime_load_script.restype = c_bool
livesplit_core_native.AutoSplittingRuntime_unload_script.argtypes = (c_void_p, )
livesplit_core_native.AutoSplittingRuntime_unload_script.restype = c_bool
livesplit_core_native.BlankSpaceComponent_new.argtypes = ()
livesplit_core_native.BlankSpaceComponent_new.restype = c_void_p
livesplit_core_native.BlankSpaceComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponent_drop.restype = None
livesplit_core_native.BlankSpaceComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponent_into_generic.restype = c_void_p
livesplit_core_native.BlankSpaceComponent_state_as_json.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponent_state_as_json.restype = c_char_p
livesplit_core_native.BlankSpaceComponent_state.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponent_state.restype = c_void_p
livesplit_core_native.BlankSpaceComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponentState_drop.restype = None
livesplit_core_native.BlankSpaceComponentState_size.argtypes = (c_void_p, )
livesplit_core_native.BlankSpaceComponentState_size.restype = c_uint32
livesplit_core_native.Component_drop.argtypes = (c_void_p, )
livesplit_core_native.Component_drop.restype = None
livesplit_core_native.CurrentComparisonComponent_new.argtypes = ()
livesplit_core_native.CurrentComparisonComponent_new.restype = c_void_p
livesplit_core_native.CurrentComparisonComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.CurrentComparisonComponent_drop.restype = None
livesplit_core_native.CurrentComparisonComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.CurrentComparisonComponent_into_generic.restype = c_void_p
livesplit_core_native.CurrentComparisonComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.CurrentComparisonComponent_state_as_json.restype = c_char_p
livesplit_core_native.CurrentComparisonComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.CurrentComparisonComponent_state.restype = c_void_p
livesplit_core_native.CurrentPaceComponent_new.argtypes = ()
livesplit_core_native.CurrentPaceComponent_new.restype = c_void_p
livesplit_core_native.CurrentPaceComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.CurrentPaceComponent_drop.restype = None
livesplit_core_native.CurrentPaceComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.CurrentPaceComponent_into_generic.restype = c_void_p
livesplit_core_native.CurrentPaceComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.CurrentPaceComponent_state_as_json.restype = c_char_p
livesplit_core_native.CurrentPaceComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.CurrentPaceComponent_state.restype = c_void_p
livesplit_core_native.DeltaComponent_new.argtypes = ()
livesplit_core_native.DeltaComponent_new.restype = c_void_p
livesplit_core_native.DeltaComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.DeltaComponent_drop.restype = None
livesplit_core_native.DeltaComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.DeltaComponent_into_generic.restype = c_void_p
livesplit_core_native.DeltaComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.DeltaComponent_state_as_json.restype = c_char_p
livesplit_core_native.DeltaComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.DeltaComponent_state.restype = c_void_p
livesplit_core_native.DetailedTimerComponent_new.argtypes = ()
livesplit_core_native.DetailedTimerComponent_new.restype = c_void_p
livesplit_core_native.DetailedTimerComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponent_drop.restype = None
livesplit_core_native.DetailedTimerComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponent_into_generic.restype = c_void_p
livesplit_core_native.DetailedTimerComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.DetailedTimerComponent_state_as_json.restype = c_char_p
livesplit_core_native.DetailedTimerComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.DetailedTimerComponent_state.restype = c_void_p
livesplit_core_native.DetailedTimerComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_drop.restype = None
livesplit_core_native.DetailedTimerComponentState_timer_time.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_timer_time.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_timer_fraction.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_timer_fraction.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_timer_semantic_color.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_timer_semantic_color.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_segment_timer_time.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_segment_timer_time.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_segment_timer_fraction.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_segment_timer_fraction.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_comparison1_visible.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison1_visible.restype = c_bool
livesplit_core_native.DetailedTimerComponentState_comparison1_name.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison1_name.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_comparison1_time.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison1_time.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_comparison2_visible.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison2_visible.restype = c_bool
livesplit_core_native.DetailedTimerComponentState_comparison2_name.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison2_name.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_comparison2_time.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_comparison2_time.restype = c_char_p
livesplit_core_native.DetailedTimerComponentState_icon_change_ptr.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_icon_change_ptr.restype = c_void_p
livesplit_core_native.DetailedTimerComponentState_icon_change_len.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_icon_change_len.restype = c_size_t
livesplit_core_native.DetailedTimerComponentState_segment_name.argtypes = (c_void_p, )
livesplit_core_native.DetailedTimerComponentState_segment_name.restype = c_char_p
livesplit_core_native.FuzzyList_new.argtypes = ()
livesplit_core_native.FuzzyList_new.restype = c_void_p
livesplit_core_native.FuzzyList_drop.argtypes = (c_void_p, )
livesplit_core_native.FuzzyList_drop.restype = None
livesplit_core_native.FuzzyList_search.argtypes = (c_void_p, c_char_p, c_size_t, )
livesplit_core_native.FuzzyList_search.restype = c_char_p
livesplit_core_native.FuzzyList_push.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.FuzzyList_push.restype = None
livesplit_core_native.GeneralLayoutSettings_default.argtypes = ()
livesplit_core_native.GeneralLayoutSettings_default.restype = c_void_p
livesplit_core_native.GeneralLayoutSettings_drop.argtypes = (c_void_p, )
livesplit_core_native.GeneralLayoutSettings_drop.restype = None
livesplit_core_native.GraphComponent_new.argtypes = ()
livesplit_core_native.GraphComponent_new.restype = c_void_p
livesplit_core_native.GraphComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.GraphComponent_drop.restype = None
livesplit_core_native.GraphComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.GraphComponent_into_generic.restype = c_void_p
livesplit_core_native.GraphComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.GraphComponent_state_as_json.restype = c_char_p
livesplit_core_native.GraphComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.GraphComponent_state.restype = c_void_p
livesplit_core_native.GraphComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_drop.restype = None
livesplit_core_native.GraphComponentState_points_len.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_points_len.restype = c_size_t
livesplit_core_native.GraphComponentState_point_x.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.GraphComponentState_point_x.restype = c_float
livesplit_core_native.GraphComponentState_point_y.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.GraphComponentState_point_y.restype = c_float
livesplit_core_native.GraphComponentState_point_is_best_segment.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.GraphComponentState_point_is_best_segment.restype = c_bool
livesplit_core_native.GraphComponentState_horizontal_grid_lines_len.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_horizontal_grid_lines_len.restype = c_size_t
livesplit_core_native.GraphComponentState_horizontal_grid_line.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.GraphComponentState_horizontal_grid_line.restype = c_float
livesplit_core_native.GraphComponentState_vertical_grid_lines_len.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_vertical_grid_lines_len.restype = c_size_t
livesplit_core_native.GraphComponentState_vertical_grid_line.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.GraphComponentState_vertical_grid_line.restype = c_float
livesplit_core_native.GraphComponentState_middle.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_middle.restype = c_float
livesplit_core_native.GraphComponentState_is_live_delta_active.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_is_live_delta_active.restype = c_bool
livesplit_core_native.GraphComponentState_is_flipped.argtypes = (c_void_p, )
livesplit_core_native.GraphComponentState_is_flipped.restype = c_bool
livesplit_core_native.HotkeyConfig_new.argtypes = ()
livesplit_core_native.HotkeyConfig_new.restype = c_void_p
livesplit_core_native.HotkeyConfig_parse_json.argtypes = (c_char_p, )
livesplit_core_native.HotkeyConfig_parse_json.restype = c_void_p
livesplit_core_native.HotkeyConfig_parse_file_handle.argtypes = (c_int64, )
livesplit_core_native.HotkeyConfig_parse_file_handle.restype = c_void_p
livesplit_core_native.HotkeyConfig_drop.argtypes = (c_void_p, )
livesplit_core_native.HotkeyConfig_drop.restype = None
livesplit_core_native.HotkeyConfig_settings_description_as_json.argtypes = (c_void_p, )
livesplit_core_native.HotkeyConfig_settings_description_as_json.restype = c_char_p
livesplit_core_native.HotkeyConfig_as_json.argtypes = (c_void_p, )
livesplit_core_native.HotkeyConfig_as_json.restype = c_char_p
livesplit_core_native.HotkeyConfig_set_value.argtypes = (c_void_p, c_size_t, c_void_p, )
livesplit_core_native.HotkeyConfig_set_value.restype = c_bool
livesplit_core_native.HotkeySystem_new.argtypes = (c_void_p, )
livesplit_core_native.HotkeySystem_new.restype = c_void_p
livesplit_core_native.HotkeySystem_with_config.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.HotkeySystem_with_config.restype = c_void_p
livesplit_core_native.HotkeySystem_drop.argtypes = (c_void_p, )
livesplit_core_native.HotkeySystem_drop.restype = None
livesplit_core_native.HotkeySystem_config.argtypes = (c_void_p, )
livesplit_core_native.HotkeySystem_config.restype = c_void_p
livesplit_core_native.HotkeySystem_resolve.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.HotkeySystem_resolve.restype = c_char_p
livesplit_core_native.HotkeySystem_deactivate.argtypes = (c_void_p, )
livesplit_core_native.HotkeySystem_deactivate.restype = c_bool
livesplit_core_native.HotkeySystem_activate.argtypes = (c_void_p, )
livesplit_core_native.HotkeySystem_activate.restype = c_bool
livesplit_core_native.HotkeySystem_set_config.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.HotkeySystem_set_config.restype = c_bool
livesplit_core_native.KeyValueComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.KeyValueComponentState_drop.restype = None
livesplit_core_native.KeyValueComponentState_key.argtypes = (c_void_p, )
livesplit_core_native.KeyValueComponentState_key.restype = c_char_p
livesplit_core_native.KeyValueComponentState_value.argtypes = (c_void_p, )
livesplit_core_native.KeyValueComponentState_value.restype = c_char_p
livesplit_core_native.KeyValueComponentState_semantic_color.argtypes = (c_void_p, )
livesplit_core_native.KeyValueComponentState_semantic_color.restype = c_char_p
livesplit_core_native.Layout_new.argtypes = ()
livesplit_core_native.Layout_new.restype = c_void_p
livesplit_core_native.Layout_default_layout.argtypes = ()
livesplit_core_native.Layout_default_layout.restype = c_void_p
livesplit_core_native.Layout_parse_json.argtypes = (c_char_p, )
livesplit_core_native.Layout_parse_json.restype = c_void_p
livesplit_core_native.Layout_parse_file_handle.argtypes = (c_int64, )
livesplit_core_native.Layout_parse_file_handle.restype = c_void_p
livesplit_core_native.Layout_parse_original_livesplit.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.Layout_parse_original_livesplit.restype = c_void_p
livesplit_core_native.Layout_drop.argtypes = (c_void_p, )
livesplit_core_native.Layout_drop.restype = None
livesplit_core_native.Layout_clone.argtypes = (c_void_p, )
livesplit_core_native.Layout_clone.restype = c_void_p
livesplit_core_native.Layout_settings_as_json.argtypes = (c_void_p, )
livesplit_core_native.Layout_settings_as_json.restype = c_char_p
livesplit_core_native.Layout_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Layout_state.restype = c_void_p
livesplit_core_native.Layout_update_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.Layout_update_state.restype = None
livesplit_core_native.Layout_update_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.Layout_update_state_as_json.restype = c_char_p
livesplit_core_native.Layout_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Layout_state_as_json.restype = c_char_p
livesplit_core_native.Layout_push.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Layout_push.restype = None
livesplit_core_native.Layout_scroll_up.argtypes = (c_void_p, )
livesplit_core_native.Layout_scroll_up.restype = None
livesplit_core_native.Layout_scroll_down.argtypes = (c_void_p, )
livesplit_core_native.Layout_scroll_down.restype = None
livesplit_core_native.Layout_remount.argtypes = (c_void_p, )
livesplit_core_native.Layout_remount.restype = None
livesplit_core_native.LayoutEditor_new.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_new.restype = c_void_p
livesplit_core_native.LayoutEditor_close.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_close.restype = c_void_p
livesplit_core_native.LayoutEditor_state_as_json.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_state_as_json.restype = c_char_p
livesplit_core_native.LayoutEditor_state.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_state.restype = c_void_p
livesplit_core_native.LayoutEditor_layout_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.LayoutEditor_layout_state_as_json.restype = c_char_p
livesplit_core_native.LayoutEditor_update_layout_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.LayoutEditor_update_layout_state.restype = None
livesplit_core_native.LayoutEditor_update_layout_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.LayoutEditor_update_layout_state_as_json.restype = c_char_p
livesplit_core_native.LayoutEditor_select.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutEditor_select.restype = None
livesplit_core_native.LayoutEditor_add_component.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.LayoutEditor_add_component.restype = None
livesplit_core_native.LayoutEditor_remove_component.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_remove_component.restype = None
livesplit_core_native.LayoutEditor_move_component_up.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_move_component_up.restype = None
livesplit_core_native.LayoutEditor_move_component_down.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_move_component_down.restype = None
livesplit_core_native.LayoutEditor_move_component.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutEditor_move_component.restype = None
livesplit_core_native.LayoutEditor_duplicate_component.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditor_duplicate_component.restype = None
livesplit_core_native.LayoutEditor_set_component_settings_value.argtypes = (c_void_p, c_size_t, c_void_p, )
livesplit_core_native.LayoutEditor_set_component_settings_value.restype = None
livesplit_core_native.LayoutEditor_set_general_settings_value.argtypes = (c_void_p, c_size_t, c_void_p, )
livesplit_core_native.LayoutEditor_set_general_settings_value.restype = None
livesplit_core_native.LayoutEditorState_drop.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditorState_drop.restype = None
livesplit_core_native.LayoutEditorState_component_len.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditorState_component_len.restype = c_size_t
livesplit_core_native.LayoutEditorState_component_text.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutEditorState_component_text.restype = c_char_p
livesplit_core_native.LayoutEditorState_buttons.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditorState_buttons.restype = c_uint8
livesplit_core_native.LayoutEditorState_selected_component.argtypes = (c_void_p, )
livesplit_core_native.LayoutEditorState_selected_component.restype = c_uint32
livesplit_core_native.LayoutEditorState_field_len.argtypes = (c_void_p, c_bool, )
livesplit_core_native.LayoutEditorState_field_len.restype = c_size_t
livesplit_core_native.LayoutEditorState_field_text.argtypes = (c_void_p, c_bool, c_size_t, )
livesplit_core_native.LayoutEditorState_field_text.restype = c_char_p
livesplit_core_native.LayoutEditorState_field_value.argtypes = (c_void_p, c_bool, c_size_t, )
livesplit_core_native.LayoutEditorState_field_value.restype = c_void_p
livesplit_core_native.LayoutState_new.argtypes = ()
livesplit_core_native.LayoutState_new.restype = c_void_p
livesplit_core_native.LayoutState_drop.argtypes = (c_void_p, )
livesplit_core_native.LayoutState_drop.restype = None
livesplit_core_native.LayoutState_as_json.argtypes = (c_void_p, )
livesplit_core_native.LayoutState_as_json.restype = c_char_p
livesplit_core_native.LayoutState_len.argtypes = (c_void_p, )
livesplit_core_native.LayoutState_len.restype = c_size_t
livesplit_core_native.LayoutState_component_type.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_type.restype = c_char_p
livesplit_core_native.LayoutState_component_as_blank_space.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_blank_space.restype = c_void_p
livesplit_core_native.LayoutState_component_as_detailed_timer.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_detailed_timer.restype = c_void_p
livesplit_core_native.LayoutState_component_as_graph.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_graph.restype = c_void_p
livesplit_core_native.LayoutState_component_as_key_value.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_key_value.restype = c_void_p
livesplit_core_native.LayoutState_component_as_separator.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_separator.restype = c_void_p
livesplit_core_native.LayoutState_component_as_splits.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_splits.restype = c_void_p
livesplit_core_native.LayoutState_component_as_text.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_text.restype = c_void_p
livesplit_core_native.LayoutState_component_as_timer.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_timer.restype = c_void_p
livesplit_core_native.LayoutState_component_as_title.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.LayoutState_component_as_title.restype = c_void_p
livesplit_core_native.ParseRunResult_drop.argtypes = (c_void_p, )
livesplit_core_native.ParseRunResult_drop.restype = None
livesplit_core_native.ParseRunResult_unwrap.argtypes = (c_void_p, )
livesplit_core_native.ParseRunResult_unwrap.restype = c_void_p
livesplit_core_native.ParseRunResult_parsed_successfully.argtypes = (c_void_p, )
livesplit_core_native.ParseRunResult_parsed_successfully.restype = c_bool
livesplit_core_native.ParseRunResult_timer_kind.argtypes = (c_void_p, )
livesplit_core_native.ParseRunResult_timer_kind.restype = c_char_p
livesplit_core_native.ParseRunResult_is_generic_timer.argtypes = (c_void_p, )
livesplit_core_native.ParseRunResult_is_generic_timer.restype = c_bool
livesplit_core_native.PbChanceComponent_new.argtypes = ()
livesplit_core_native.PbChanceComponent_new.restype = c_void_p
livesplit_core_native.PbChanceComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.PbChanceComponent_drop.restype = None
livesplit_core_native.PbChanceComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.PbChanceComponent_into_generic.restype = c_void_p
livesplit_core_native.PbChanceComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.PbChanceComponent_state_as_json.restype = c_char_p
livesplit_core_native.PbChanceComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.PbChanceComponent_state.restype = c_void_p
livesplit_core_native.PossibleTimeSaveComponent_new.argtypes = ()
livesplit_core_native.PossibleTimeSaveComponent_new.restype = c_void_p
livesplit_core_native.PossibleTimeSaveComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.PossibleTimeSaveComponent_drop.restype = None
livesplit_core_native.PossibleTimeSaveComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.PossibleTimeSaveComponent_into_generic.restype = c_void_p
livesplit_core_native.PossibleTimeSaveComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.PossibleTimeSaveComponent_state_as_json.restype = c_char_p
livesplit_core_native.PossibleTimeSaveComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.PossibleTimeSaveComponent_state.restype = c_void_p
livesplit_core_native.PotentialCleanUp_drop.argtypes = (c_void_p, )
livesplit_core_native.PotentialCleanUp_drop.restype = None
livesplit_core_native.PotentialCleanUp_message.argtypes = (c_void_p, )
livesplit_core_native.PotentialCleanUp_message.restype = c_char_p
livesplit_core_native.PreviousSegmentComponent_new.argtypes = ()
livesplit_core_native.PreviousSegmentComponent_new.restype = c_void_p
livesplit_core_native.PreviousSegmentComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.PreviousSegmentComponent_drop.restype = None
livesplit_core_native.PreviousSegmentComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.PreviousSegmentComponent_into_generic.restype = c_void_p
livesplit_core_native.PreviousSegmentComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.PreviousSegmentComponent_state_as_json.restype = c_char_p
livesplit_core_native.PreviousSegmentComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.PreviousSegmentComponent_state.restype = c_void_p
livesplit_core_native.Run_new.argtypes = ()
livesplit_core_native.Run_new.restype = c_void_p
livesplit_core_native.Run_parse.argtypes = (c_void_p, c_size_t, c_char_p, )
livesplit_core_native.Run_parse.restype = c_void_p
livesplit_core_native.Run_parse_file_handle.argtypes = (c_int64, c_char_p, )
livesplit_core_native.Run_parse_file_handle.restype = c_void_p
livesplit_core_native.Run_drop.argtypes = (c_void_p, )
livesplit_core_native.Run_drop.restype = None
livesplit_core_native.Run_clone.argtypes = (c_void_p, )
livesplit_core_native.Run_clone.restype = c_void_p
livesplit_core_native.Run_game_name.argtypes = (c_void_p, )
livesplit_core_native.Run_game_name.restype = c_char_p
livesplit_core_native.Run_game_icon_ptr.argtypes = (c_void_p, )
livesplit_core_native.Run_game_icon_ptr.restype = c_void_p
livesplit_core_native.Run_game_icon_len.argtypes = (c_void_p, )
livesplit_core_native.Run_game_icon_len.restype = c_size_t
livesplit_core_native.Run_category_name.argtypes = (c_void_p, )
livesplit_core_native.Run_category_name.restype = c_char_p
livesplit_core_native.Run_extended_file_name.argtypes = (c_void_p, c_bool, )
livesplit_core_native.Run_extended_file_name.restype = c_char_p
livesplit_core_native.Run_extended_name.argtypes = (c_void_p, c_bool, )
livesplit_core_native.Run_extended_name.restype = c_char_p
livesplit_core_native.Run_extended_category_name.argtypes = (c_void_p, c_bool, c_bool, c_bool, )
livesplit_core_native.Run_extended_category_name.restype = c_char_p
livesplit_core_native.Run_attempt_count.argtypes = (c_void_p, )
livesplit_core_native.Run_attempt_count.restype = c_uint32
livesplit_core_native.Run_metadata.argtypes = (c_void_p, )
livesplit_core_native.Run_metadata.restype = c_void_p
livesplit_core_native.Run_offset.argtypes = (c_void_p, )
livesplit_core_native.Run_offset.restype = c_void_p
livesplit_core_native.Run_len.argtypes = (c_void_p, )
livesplit_core_native.Run_len.restype = c_size_t
livesplit_core_native.Run_has_been_modified.argtypes = (c_void_p, )
livesplit_core_native.Run_has_been_modified.restype = c_bool
livesplit_core_native.Run_segment.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.Run_segment.restype = c_void_p
livesplit_core_native.Run_attempt_history_len.argtypes = (c_void_p, )
livesplit_core_native.Run_attempt_history_len.restype = c_size_t
livesplit_core_native.Run_attempt_history_index.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.Run_attempt_history_index.restype = c_void_p
livesplit_core_native.Run_save_as_lss.argtypes = (c_void_p, )
livesplit_core_native.Run_save_as_lss.restype = c_char_p
livesplit_core_native.Run_custom_comparisons_len.argtypes = (c_void_p, )
livesplit_core_native.Run_custom_comparisons_len.restype = c_size_t
livesplit_core_native.Run_custom_comparison.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.Run_custom_comparison.restype = c_char_p
livesplit_core_native.Run_auto_splitter_settings.argtypes = (c_void_p, )
livesplit_core_native.Run_auto_splitter_settings.restype = c_char_p
livesplit_core_native.Run_push_segment.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Run_push_segment.restype = None
livesplit_core_native.Run_set_game_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.Run_set_game_name.restype = None
livesplit_core_native.Run_set_category_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.Run_set_category_name.restype = None
livesplit_core_native.Run_mark_as_modified.argtypes = (c_void_p, )
livesplit_core_native.Run_mark_as_modified.restype = None
livesplit_core_native.RunEditor_new.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_new.restype = c_void_p
livesplit_core_native.RunEditor_close.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_close.restype = c_void_p
livesplit_core_native.RunEditor_state_as_json.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_state_as_json.restype = c_char_p
livesplit_core_native.RunEditor_select_timing_method.argtypes = (c_void_p, c_uint8, )
livesplit_core_native.RunEditor_select_timing_method.restype = None
livesplit_core_native.RunEditor_unselect.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.RunEditor_unselect.restype = None
livesplit_core_native.RunEditor_select_additionally.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.RunEditor_select_additionally.restype = None
livesplit_core_native.RunEditor_select_only.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.RunEditor_select_only.restype = None
livesplit_core_native.RunEditor_set_game_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_set_game_name.restype = None
livesplit_core_native.RunEditor_set_category_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_set_category_name.restype = None
livesplit_core_native.RunEditor_parse_and_set_offset.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_parse_and_set_offset.restype = c_bool
livesplit_core_native.RunEditor_parse_and_set_attempt_count.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_parse_and_set_attempt_count.restype = c_bool
livesplit_core_native.RunEditor_set_game_icon.argtypes = (c_void_p, c_void_p, c_size_t, )
livesplit_core_native.RunEditor_set_game_icon.restype = None
livesplit_core_native.RunEditor_remove_game_icon.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_remove_game_icon.restype = None
livesplit_core_native.RunEditor_set_run_id.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_set_run_id.restype = None
livesplit_core_native.RunEditor_set_region_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_set_region_name.restype = None
livesplit_core_native.RunEditor_set_platform_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_set_platform_name.restype = None
livesplit_core_native.RunEditor_set_emulator_usage.argtypes = (c_void_p, c_bool, )
livesplit_core_native.RunEditor_set_emulator_usage.restype = None
livesplit_core_native.RunEditor_set_speedrun_com_variable.argtypes = (c_void_p, c_char_p, c_char_p, )
livesplit_core_native.RunEditor_set_speedrun_com_variable.restype = None
livesplit_core_native.RunEditor_remove_speedrun_com_variable.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_remove_speedrun_com_variable.restype = None
livesplit_core_native.RunEditor_add_custom_variable.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_add_custom_variable.restype = None
livesplit_core_native.RunEditor_set_custom_variable.argtypes = (c_void_p, c_char_p, c_char_p, )
livesplit_core_native.RunEditor_set_custom_variable.restype = None
livesplit_core_native.RunEditor_remove_custom_variable.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_remove_custom_variable.restype = None
livesplit_core_native.RunEditor_clear_metadata.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_clear_metadata.restype = None
livesplit_core_native.RunEditor_insert_segment_above.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_insert_segment_above.restype = None
livesplit_core_native.RunEditor_insert_segment_below.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_insert_segment_below.restype = None
livesplit_core_native.RunEditor_remove_segments.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_remove_segments.restype = None
livesplit_core_native.RunEditor_move_segments_up.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_move_segments_up.restype = None
livesplit_core_native.RunEditor_move_segments_down.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_move_segments_down.restype = None
livesplit_core_native.RunEditor_active_set_icon.argtypes = (c_void_p, c_void_p, c_size_t, )
livesplit_core_native.RunEditor_active_set_icon.restype = None
livesplit_core_native.RunEditor_active_remove_icon.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_active_remove_icon.restype = None
livesplit_core_native.RunEditor_active_set_name.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_active_set_name.restype = None
livesplit_core_native.RunEditor_active_parse_and_set_split_time.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_active_parse_and_set_split_time.restype = c_bool
livesplit_core_native.RunEditor_active_parse_and_set_segment_time.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_active_parse_and_set_segment_time.restype = c_bool
livesplit_core_native.RunEditor_active_parse_and_set_best_segment_time.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_active_parse_and_set_best_segment_time.restype = c_bool
livesplit_core_native.RunEditor_active_parse_and_set_comparison_time.argtypes = (c_void_p, c_char_p, c_char_p, )
livesplit_core_native.RunEditor_active_parse_and_set_comparison_time.restype = c_bool
livesplit_core_native.RunEditor_add_comparison.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_add_comparison.restype = c_bool
livesplit_core_native.RunEditor_import_comparison.argtypes = (c_void_p, c_void_p, c_char_p, )
livesplit_core_native.RunEditor_import_comparison.restype = c_bool
livesplit_core_native.RunEditor_remove_comparison.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_remove_comparison.restype = None
livesplit_core_native.RunEditor_rename_comparison.argtypes = (c_void_p, c_char_p, c_char_p, )
livesplit_core_native.RunEditor_rename_comparison.restype = c_bool
livesplit_core_native.RunEditor_move_comparison.argtypes = (c_void_p, c_size_t, c_size_t, )
livesplit_core_native.RunEditor_move_comparison.restype = c_bool
livesplit_core_native.RunEditor_parse_and_generate_goal_comparison.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.RunEditor_parse_and_generate_goal_comparison.restype = c_bool
livesplit_core_native.RunEditor_clear_history.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_clear_history.restype = None
livesplit_core_native.RunEditor_clear_times.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_clear_times.restype = None
livesplit_core_native.RunEditor_clean_sum_of_best.argtypes = (c_void_p, )
livesplit_core_native.RunEditor_clean_sum_of_best.restype = c_void_p
livesplit_core_native.RunMetadata_run_id.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_run_id.restype = c_char_p
livesplit_core_native.RunMetadata_platform_name.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_platform_name.restype = c_char_p
livesplit_core_native.RunMetadata_uses_emulator.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_uses_emulator.restype = c_bool
livesplit_core_native.RunMetadata_region_name.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_region_name.restype = c_char_p
livesplit_core_native.RunMetadata_speedrun_com_variables.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_speedrun_com_variables.restype = c_void_p
livesplit_core_native.RunMetadata_custom_variables.argtypes = (c_void_p, )
livesplit_core_native.RunMetadata_custom_variables.restype = c_void_p
livesplit_core_native.RunMetadataCustomVariable_drop.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariable_drop.restype = None
livesplit_core_native.RunMetadataCustomVariable_name.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariable_name.restype = c_char_p
livesplit_core_native.RunMetadataCustomVariable_value.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariable_value.restype = c_char_p
livesplit_core_native.RunMetadataCustomVariable_is_permanent.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariable_is_permanent.restype = c_bool
livesplit_core_native.RunMetadataCustomVariablesIter_drop.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariablesIter_drop.restype = None
livesplit_core_native.RunMetadataCustomVariablesIter_next.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataCustomVariablesIter_next.restype = c_void_p
livesplit_core_native.RunMetadataSpeedrunComVariable_drop.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataSpeedrunComVariable_drop.restype = None
livesplit_core_native.RunMetadataSpeedrunComVariable_name.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataSpeedrunComVariable_name.restype = c_char_p
livesplit_core_native.RunMetadataSpeedrunComVariable_value.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataSpeedrunComVariable_value.restype = c_char_p
livesplit_core_native.RunMetadataSpeedrunComVariablesIter_drop.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataSpeedrunComVariablesIter_drop.restype = None
livesplit_core_native.RunMetadataSpeedrunComVariablesIter_next.argtypes = (c_void_p, )
livesplit_core_native.RunMetadataSpeedrunComVariablesIter_next.restype = c_void_p
livesplit_core_native.Segment_new.argtypes = (c_char_p, )
livesplit_core_native.Segment_new.restype = c_void_p
livesplit_core_native.Segment_drop.argtypes = (c_void_p, )
livesplit_core_native.Segment_drop.restype = None
livesplit_core_native.Segment_name.argtypes = (c_void_p, )
livesplit_core_native.Segment_name.restype = c_char_p
livesplit_core_native.Segment_icon_ptr.argtypes = (c_void_p, )
livesplit_core_native.Segment_icon_ptr.restype = c_void_p
livesplit_core_native.Segment_icon_len.argtypes = (c_void_p, )
livesplit_core_native.Segment_icon_len.restype = c_size_t
livesplit_core_native.Segment_comparison.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.Segment_comparison.restype = c_void_p
livesplit_core_native.Segment_personal_best_split_time.argtypes = (c_void_p, )
livesplit_core_native.Segment_personal_best_split_time.restype = c_void_p
livesplit_core_native.Segment_best_segment_time.argtypes = (c_void_p, )
livesplit_core_native.Segment_best_segment_time.restype = c_void_p
livesplit_core_native.Segment_segment_history.argtypes = (c_void_p, )
livesplit_core_native.Segment_segment_history.restype = c_void_p
livesplit_core_native.SegmentHistory_iter.argtypes = (c_void_p, )
livesplit_core_native.SegmentHistory_iter.restype = c_void_p
livesplit_core_native.SegmentHistoryElement_index.argtypes = (c_void_p, )
livesplit_core_native.SegmentHistoryElement_index.restype = c_int32
livesplit_core_native.SegmentHistoryElement_time.argtypes = (c_void_p, )
livesplit_core_native.SegmentHistoryElement_time.restype = c_void_p
livesplit_core_native.SegmentHistoryIter_drop.argtypes = (c_void_p, )
livesplit_core_native.SegmentHistoryIter_drop.restype = None
livesplit_core_native.SegmentHistoryIter_next.argtypes = (c_void_p, )
livesplit_core_native.SegmentHistoryIter_next.restype = c_void_p
livesplit_core_native.SegmentTimeComponent_new.argtypes = ()
livesplit_core_native.SegmentTimeComponent_new.restype = c_void_p
livesplit_core_native.SegmentTimeComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.SegmentTimeComponent_drop.restype = None
livesplit_core_native.SegmentTimeComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.SegmentTimeComponent_into_generic.restype = c_void_p
livesplit_core_native.SegmentTimeComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SegmentTimeComponent_state_as_json.restype = c_char_p
livesplit_core_native.SegmentTimeComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SegmentTimeComponent_state.restype = c_void_p
livesplit_core_native.SeparatorComponent_new.argtypes = ()
livesplit_core_native.SeparatorComponent_new.restype = c_void_p
livesplit_core_native.SeparatorComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.SeparatorComponent_drop.restype = None
livesplit_core_native.SeparatorComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.SeparatorComponent_into_generic.restype = c_void_p
livesplit_core_native.SeparatorComponent_state.argtypes = (c_void_p, )
livesplit_core_native.SeparatorComponent_state.restype = c_void_p
livesplit_core_native.SeparatorComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.SeparatorComponentState_drop.restype = None
livesplit_core_native.SettingValue_from_bool.argtypes = (c_bool, )
livesplit_core_native.SettingValue_from_bool.restype = c_void_p
livesplit_core_native.SettingValue_from_uint.argtypes = (c_uint32, )
livesplit_core_native.SettingValue_from_uint.restype = c_void_p
livesplit_core_native.SettingValue_from_int.argtypes = (c_int32, )
livesplit_core_native.SettingValue_from_int.restype = c_void_p
livesplit_core_native.SettingValue_from_string.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_string.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_string.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_optional_string.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_empty_string.argtypes = ()
livesplit_core_native.SettingValue_from_optional_empty_string.restype = c_void_p
livesplit_core_native.SettingValue_from_accuracy.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_accuracy.restype = c_void_p
livesplit_core_native.SettingValue_from_digits_format.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_digits_format.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_timing_method.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_optional_timing_method.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_empty_timing_method.argtypes = ()
livesplit_core_native.SettingValue_from_optional_empty_timing_method.restype = c_void_p
livesplit_core_native.SettingValue_from_color.argtypes = (c_float, c_float, c_float, c_float, )
livesplit_core_native.SettingValue_from_color.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_color.argtypes = (c_float, c_float, c_float, c_float, )
livesplit_core_native.SettingValue_from_optional_color.restype = c_void_p
livesplit_core_native.SettingValue_from_optional_empty_color.argtypes = ()
livesplit_core_native.SettingValue_from_optional_empty_color.restype = c_void_p
livesplit_core_native.SettingValue_from_transparent_gradient.argtypes = ()
livesplit_core_native.SettingValue_from_transparent_gradient.restype = c_void_p
livesplit_core_native.SettingValue_from_vertical_gradient.argtypes = (c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, )
livesplit_core_native.SettingValue_from_vertical_gradient.restype = c_void_p
livesplit_core_native.SettingValue_from_horizontal_gradient.argtypes = (c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, )
livesplit_core_native.SettingValue_from_horizontal_gradient.restype = c_void_p
livesplit_core_native.SettingValue_from_alternating_gradient.argtypes = (c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, )
livesplit_core_native.SettingValue_from_alternating_gradient.restype = c_void_p
livesplit_core_native.SettingValue_from_alignment.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_alignment.restype = c_void_p
livesplit_core_native.SettingValue_from_column_kind.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_column_kind.restype = c_void_p
livesplit_core_native.SettingValue_from_column_start_with.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_column_start_with.restype = c_void_p
livesplit_core_native.SettingValue_from_column_update_with.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_column_update_with.restype = c_void_p
livesplit_core_native.SettingValue_from_column_update_trigger.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_column_update_trigger.restype = c_void_p
livesplit_core_native.SettingValue_from_layout_direction.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_layout_direction.restype = c_void_p
livesplit_core_native.SettingValue_from_font.argtypes = (c_char_p, c_char_p, c_char_p, c_char_p, )
livesplit_core_native.SettingValue_from_font.restype = c_void_p
livesplit_core_native.SettingValue_from_empty_font.argtypes = ()
livesplit_core_native.SettingValue_from_empty_font.restype = c_void_p
livesplit_core_native.SettingValue_from_delta_gradient.argtypes = (c_char_p, )
livesplit_core_native.SettingValue_from_delta_gradient.restype = c_void_p
livesplit_core_native.SettingValue_drop.argtypes = (c_void_p, )
livesplit_core_native.SettingValue_drop.restype = None
livesplit_core_native.SettingValue_as_json.argtypes = (c_void_p, )
livesplit_core_native.SettingValue_as_json.restype = c_char_p
livesplit_core_native.SharedTimer_drop.argtypes = (c_void_p, )
livesplit_core_native.SharedTimer_drop.restype = None
livesplit_core_native.SharedTimer_share.argtypes = (c_void_p, )
livesplit_core_native.SharedTimer_share.restype = c_void_p
livesplit_core_native.SharedTimer_read.argtypes = (c_void_p, )
livesplit_core_native.SharedTimer_read.restype = c_void_p
livesplit_core_native.SharedTimer_write.argtypes = (c_void_p, )
livesplit_core_native.SharedTimer_write.restype = c_void_p
livesplit_core_native.SharedTimer_replace_inner.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SharedTimer_replace_inner.restype = None
livesplit_core_native.SoftwareRenderer_new.argtypes = ()
livesplit_core_native.SoftwareRenderer_new.restype = c_void_p
livesplit_core_native.SoftwareRenderer_drop.argtypes = (c_void_p, )
livesplit_core_native.SoftwareRenderer_drop.restype = None
livesplit_core_native.SoftwareRenderer_render.argtypes = (c_void_p, c_void_p, c_void_p, c_uint32, c_uint32, c_uint32, c_bool, )
livesplit_core_native.SoftwareRenderer_render.restype = None
livesplit_core_native.SplitsComponent_new.argtypes = ()
livesplit_core_native.SplitsComponent_new.restype = c_void_p
livesplit_core_native.SplitsComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponent_drop.restype = None
livesplit_core_native.SplitsComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponent_into_generic.restype = c_void_p
livesplit_core_native.SplitsComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.SplitsComponent_state_as_json.restype = c_char_p
livesplit_core_native.SplitsComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.SplitsComponent_state.restype = c_void_p
livesplit_core_native.SplitsComponent_scroll_up.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponent_scroll_up.restype = None
livesplit_core_native.SplitsComponent_scroll_down.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponent_scroll_down.restype = None
livesplit_core_native.SplitsComponent_set_visual_split_count.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponent_set_visual_split_count.restype = None
livesplit_core_native.SplitsComponent_set_split_preview_count.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponent_set_split_preview_count.restype = None
livesplit_core_native.SplitsComponent_set_always_show_last_split.argtypes = (c_void_p, c_bool, )
livesplit_core_native.SplitsComponent_set_always_show_last_split.restype = None
livesplit_core_native.SplitsComponent_set_separator_last_split.argtypes = (c_void_p, c_bool, )
livesplit_core_native.SplitsComponent_set_separator_last_split.restype = None
livesplit_core_native.SplitsComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponentState_drop.restype = None
livesplit_core_native.SplitsComponentState_final_separator_shown.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponentState_final_separator_shown.restype = c_bool
livesplit_core_native.SplitsComponentState_len.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponentState_len.restype = c_size_t
livesplit_core_native.SplitsComponentState_icon_change_count.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponentState_icon_change_count.restype = c_size_t
livesplit_core_native.SplitsComponentState_icon_change_segment_index.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_icon_change_segment_index.restype = c_size_t
livesplit_core_native.SplitsComponentState_icon_change_icon_ptr.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_icon_change_icon_ptr.restype = c_void_p
livesplit_core_native.SplitsComponentState_icon_change_icon_len.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_icon_change_icon_len.restype = c_size_t
livesplit_core_native.SplitsComponentState_name.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_name.restype = c_char_p
livesplit_core_native.SplitsComponentState_columns_len.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_columns_len.restype = c_size_t
livesplit_core_native.SplitsComponentState_column_value.argtypes = (c_void_p, c_size_t, c_size_t, )
livesplit_core_native.SplitsComponentState_column_value.restype = c_char_p
livesplit_core_native.SplitsComponentState_column_semantic_color.argtypes = (c_void_p, c_size_t, c_size_t, )
livesplit_core_native.SplitsComponentState_column_semantic_color.restype = c_char_p
livesplit_core_native.SplitsComponentState_is_current_split.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_is_current_split.restype = c_bool
livesplit_core_native.SplitsComponentState_has_column_labels.argtypes = (c_void_p, )
livesplit_core_native.SplitsComponentState_has_column_labels.restype = c_bool
livesplit_core_native.SplitsComponentState_column_label.argtypes = (c_void_p, c_size_t, )
livesplit_core_native.SplitsComponentState_column_label.restype = c_char_p
livesplit_core_native.SumOfBestCleaner_drop.argtypes = (c_void_p, )
livesplit_core_native.SumOfBestCleaner_drop.restype = None
livesplit_core_native.SumOfBestCleaner_next_potential_clean_up.argtypes = (c_void_p, )
livesplit_core_native.SumOfBestCleaner_next_potential_clean_up.restype = c_void_p
livesplit_core_native.SumOfBestCleaner_apply.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SumOfBestCleaner_apply.restype = None
livesplit_core_native.SumOfBestComponent_new.argtypes = ()
livesplit_core_native.SumOfBestComponent_new.restype = c_void_p
livesplit_core_native.SumOfBestComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.SumOfBestComponent_drop.restype = None
livesplit_core_native.SumOfBestComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.SumOfBestComponent_into_generic.restype = c_void_p
livesplit_core_native.SumOfBestComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SumOfBestComponent_state_as_json.restype = c_char_p
livesplit_core_native.SumOfBestComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.SumOfBestComponent_state.restype = c_void_p
livesplit_core_native.TextComponent_new.argtypes = ()
livesplit_core_native.TextComponent_new.restype = c_void_p
livesplit_core_native.TextComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.TextComponent_drop.restype = None
livesplit_core_native.TextComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.TextComponent_into_generic.restype = c_void_p
livesplit_core_native.TextComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TextComponent_state_as_json.restype = c_char_p
livesplit_core_native.TextComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TextComponent_state.restype = c_void_p
livesplit_core_native.TextComponent_set_center.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.TextComponent_set_center.restype = None
livesplit_core_native.TextComponent_set_left.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.TextComponent_set_left.restype = None
livesplit_core_native.TextComponent_set_right.argtypes = (c_void_p, c_char_p, )
livesplit_core_native.TextComponent_set_right.restype = None
livesplit_core_native.TextComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.TextComponentState_drop.restype = None
livesplit_core_native.TextComponentState_left.argtypes = (c_void_p, )
livesplit_core_native.TextComponentState_left.restype = c_char_p
livesplit_core_native.TextComponentState_right.argtypes = (c_void_p, )
livesplit_core_native.TextComponentState_right.restype = c_char_p
livesplit_core_native.TextComponentState_center.argtypes = (c_void_p, )
livesplit_core_native.TextComponentState_center.restype = c_char_p
livesplit_core_native.TextComponentState_is_split.argtypes = (c_void_p, )
livesplit_core_native.TextComponentState_is_split.restype = c_bool
livesplit_core_native.Time_drop.argtypes = (c_void_p, )
livesplit_core_native.Time_drop.restype = None
livesplit_core_native.Time_clone.argtypes = (c_void_p, )
livesplit_core_native.Time_clone.restype = c_void_p
livesplit_core_native.Time_real_time.argtypes = (c_void_p, )
livesplit_core_native.Time_real_time.restype = c_void_p
livesplit_core_native.Time_game_time.argtypes = (c_void_p, )
livesplit_core_native.Time_game_time.restype = c_void_p
livesplit_core_native.Time_index.argtypes = (c_void_p, c_uint8, )
livesplit_core_native.Time_index.restype = c_void_p
livesplit_core_native.TimeSpan_from_seconds.argtypes = (c_double, )
livesplit_core_native.TimeSpan_from_seconds.restype = c_void_p
livesplit_core_native.TimeSpan_parse.argtypes = (c_char_p, )
livesplit_core_native.TimeSpan_parse.restype = c_void_p
livesplit_core_native.TimeSpan_drop.argtypes = (c_void_p, )
livesplit_core_native.TimeSpan_drop.restype = None
livesplit_core_native.TimeSpan_clone.argtypes = (c_void_p, )
livesplit_core_native.TimeSpan_clone.restype = c_void_p
livesplit_core_native.TimeSpan_total_seconds.argtypes = (c_void_p, )
livesplit_core_native.TimeSpan_total_seconds.restype = c_double
livesplit_core_native.Timer_new.argtypes = (c_void_p, )
livesplit_core_native.Timer_new.restype = c_void_p
livesplit_core_native.Timer_into_shared.argtypes = (c_void_p, )
livesplit_core_native.Timer_into_shared.restype = c_void_p
livesplit_core_native.Timer_into_run.argtypes = (c_void_p, c_bool, )
livesplit_core_native.Timer_into_run.restype = c_void_p
livesplit_core_native.Timer_drop.argtypes = (c_void_p, )
livesplit_core_native.Timer_drop.restype = None
livesplit_core_native.Timer_current_split_index.argtypes = (c_void_p, )
livesplit_core_native.Timer_current_split_index.restype = c_ssize_t
livesplit_core_native.Timer_current_timing_method.argtypes = (c_void_p, )
livesplit_core_native.Timer_current_timing_method.restype = c_uint8
livesplit_core_native.Timer_current_comparison.argtypes = (c_void_p, )
livesplit_core_native.Timer_current_comparison.restype = c_char_p
livesplit_core_native.Timer_is_game_time_initialized.argtypes = (c_void_p, )
livesplit_core_native.Timer_is_game_time_initialized.restype = c_bool
livesplit_core_native.Timer_is_game_time_paused.argtypes = (c_void_p, )
livesplit_core_native.Timer_is_game_time_paused.restype = c_bool
livesplit_core_native.Timer_loading_times.argtypes = (c_void_p, )
livesplit_core_native.Timer_loading_times.restype = c_void_p
livesplit_core_native.Timer_current_phase.argtypes = (c_void_p, )
livesplit_core_native.Timer_current_phase.restype = c_uint8
livesplit_core_native.Timer_get_run.argtypes = (c_void_p, )
livesplit_core_native.Timer_get_run.restype = c_void_p
livesplit_core_native.Timer_save_as_lss.argtypes = (c_void_p, )
livesplit_core_native.Timer_save_as_lss.restype = c_char_p
livesplit_core_native.Timer_print_debug.argtypes = (c_void_p, )
livesplit_core_native.Timer_print_debug.restype = None
livesplit_core_native.Timer_current_time.argtypes = (c_void_p, )
livesplit_core_native.Timer_current_time.restype = c_void_p
livesplit_core_native.Timer_replace_run.argtypes = (c_void_p, c_void_p, c_bool, )
livesplit_core_native.Timer_replace_run.restype = c_bool
livesplit_core_native.Timer_set_run.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Timer_set_run.restype = c_void_p
livesplit_core_native.Timer_start.argtypes = (c_void_p, )
livesplit_core_native.Timer_start.restype = None
livesplit_core_native.Timer_split.argtypes = (c_void_p, )
livesplit_core_native.Timer_split.restype = None
livesplit_core_native.Timer_split_or_start.argtypes = (c_void_p, )
livesplit_core_native.Timer_split_or_start.restype = None
livesplit_core_native.Timer_skip_split.argtypes = (c_void_p, )
livesplit_core_native.Timer_skip_split.restype = None
livesplit_core_native.Timer_undo_split.argtypes = (c_void_p, )
livesplit_core_native.Timer_undo_split.restype = None
livesplit_core_native.Timer_reset.argtypes = (c_void_p, c_bool, )
livesplit_core_native.Timer_reset.restype = None
livesplit_core_native.Timer_reset_and_set_attempt_as_pb.argtypes = (c_void_p, )
livesplit_core_native.Timer_reset_and_set_attempt_as_pb.restype = None
livesplit_core_native.Timer_pause.argtypes = (c_void_p, )
livesplit_core_native.Timer_pause.restype = None
livesplit_core_native.Timer_resume.argtypes = (c_void_p, )
livesplit_core_native.Timer_resume.restype = None
livesplit_core_native.Timer_toggle_pause.argtypes = (c_void_p, )
livesplit_core_native.Timer_toggle_pause.restype = None
livesplit_core_native.Timer_toggle_pause_or_start.argtypes = (c_void_p, )
livesplit_core_native.Timer_toggle_pause_or_start.restype = None
livesplit_core_native.Timer_undo_all_pauses.argtypes = (c_void_p, )
livesplit_core_native.Timer_undo_all_pauses.restype = None
livesplit_core_native.Timer_set_current_timing_method.argtypes = (c_void_p, c_uint8, )
livesplit_core_native.Timer_set_current_timing_method.restype = None
livesplit_core_native.Timer_switch_to_next_comparison.argtypes = (c_void_p, )
livesplit_core_native.Timer_switch_to_next_comparison.restype = None
livesplit_core_native.Timer_switch_to_previous_comparison.argtypes = (c_void_p, )
livesplit_core_native.Timer_switch_to_previous_comparison.restype = None
livesplit_core_native.Timer_initialize_game_time.argtypes = (c_void_p, )
livesplit_core_native.Timer_initialize_game_time.restype = None
livesplit_core_native.Timer_deinitialize_game_time.argtypes = (c_void_p, )
livesplit_core_native.Timer_deinitialize_game_time.restype = None
livesplit_core_native.Timer_pause_game_time.argtypes = (c_void_p, )
livesplit_core_native.Timer_pause_game_time.restype = None
livesplit_core_native.Timer_resume_game_time.argtypes = (c_void_p, )
livesplit_core_native.Timer_resume_game_time.restype = None
livesplit_core_native.Timer_set_game_time.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Timer_set_game_time.restype = None
livesplit_core_native.Timer_set_loading_times.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.Timer_set_loading_times.restype = None
livesplit_core_native.Timer_mark_as_unmodified.argtypes = (c_void_p, )
livesplit_core_native.Timer_mark_as_unmodified.restype = None
livesplit_core_native.TimerComponent_new.argtypes = ()
livesplit_core_native.TimerComponent_new.restype = c_void_p
livesplit_core_native.TimerComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.TimerComponent_drop.restype = None
livesplit_core_native.TimerComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.TimerComponent_into_generic.restype = c_void_p
livesplit_core_native.TimerComponent_state_as_json.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.TimerComponent_state_as_json.restype = c_char_p
livesplit_core_native.TimerComponent_state.argtypes = (c_void_p, c_void_p, c_void_p, )
livesplit_core_native.TimerComponent_state.restype = c_void_p
livesplit_core_native.TimerComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.TimerComponentState_drop.restype = None
livesplit_core_native.TimerComponentState_time.argtypes = (c_void_p, )
livesplit_core_native.TimerComponentState_time.restype = c_char_p
livesplit_core_native.TimerComponentState_fraction.argtypes = (c_void_p, )
livesplit_core_native.TimerComponentState_fraction.restype = c_char_p
livesplit_core_native.TimerComponentState_semantic_color.argtypes = (c_void_p, )
livesplit_core_native.TimerComponentState_semantic_color.restype = c_char_p
livesplit_core_native.TimerReadLock_drop.argtypes = (c_void_p, )
livesplit_core_native.TimerReadLock_drop.restype = None
livesplit_core_native.TimerReadLock_timer.argtypes = (c_void_p, )
livesplit_core_native.TimerReadLock_timer.restype = c_void_p
livesplit_core_native.TimerWriteLock_drop.argtypes = (c_void_p, )
livesplit_core_native.TimerWriteLock_drop.restype = None
livesplit_core_native.TimerWriteLock_timer.argtypes = (c_void_p, )
livesplit_core_native.TimerWriteLock_timer.restype = c_void_p
livesplit_core_native.TitleComponent_new.argtypes = ()
livesplit_core_native.TitleComponent_new.restype = c_void_p
livesplit_core_native.TitleComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.TitleComponent_drop.restype = None
livesplit_core_native.TitleComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.TitleComponent_into_generic.restype = c_void_p
livesplit_core_native.TitleComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TitleComponent_state_as_json.restype = c_char_p
livesplit_core_native.TitleComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TitleComponent_state.restype = c_void_p
livesplit_core_native.TitleComponentState_drop.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_drop.restype = None
livesplit_core_native.TitleComponentState_icon_change_ptr.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_icon_change_ptr.restype = c_void_p
livesplit_core_native.TitleComponentState_icon_change_len.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_icon_change_len.restype = c_size_t
livesplit_core_native.TitleComponentState_line1.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_line1.restype = c_char_p
livesplit_core_native.TitleComponentState_line2.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_line2.restype = c_char_p
livesplit_core_native.TitleComponentState_is_centered.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_is_centered.restype = c_bool
livesplit_core_native.TitleComponentState_shows_finished_runs.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_shows_finished_runs.restype = c_bool
livesplit_core_native.TitleComponentState_finished_runs.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_finished_runs.restype = c_uint32
livesplit_core_native.TitleComponentState_shows_attempts.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_shows_attempts.restype = c_bool
livesplit_core_native.TitleComponentState_attempts.argtypes = (c_void_p, )
livesplit_core_native.TitleComponentState_attempts.restype = c_uint32
livesplit_core_native.TotalPlaytimeComponent_new.argtypes = ()
livesplit_core_native.TotalPlaytimeComponent_new.restype = c_void_p
livesplit_core_native.TotalPlaytimeComponent_drop.argtypes = (c_void_p, )
livesplit_core_native.TotalPlaytimeComponent_drop.restype = None
livesplit_core_native.TotalPlaytimeComponent_into_generic.argtypes = (c_void_p, )
livesplit_core_native.TotalPlaytimeComponent_into_generic.restype = c_void_p
livesplit_core_native.TotalPlaytimeComponent_state_as_json.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TotalPlaytimeComponent_state_as_json.restype = c_char_p
livesplit_core_native.TotalPlaytimeComponent_state.argtypes = (c_void_p, c_void_p, )
livesplit_core_native.TotalPlaytimeComponent_state.restype = c_void_p

class AnalysisRef:
    """The analysis module provides a variety of functions for calculating
    information about runs.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class AnalysisRefMut(AnalysisRef):
    """The analysis module provides a variety of functions for calculating
    information about runs.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class Analysis(AnalysisRefMut):
    """The analysis module provides a variety of functions for calculating
    information about runs.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def calculate_sum_of_best(run, simple_calculation, use_current_run, method):
        """Calculates the Sum of Best Segments for the timing method provided. This is
        the fastest time possible to complete a run of a category, based on
        information collected from all the previous attempts. This often matches up
        with the sum of the best segment times of all the segments, but that may not
        always be the case, as skipped segments may introduce combined segments that
        may be faster than the actual sum of their best segment times. The name is
        therefore a bit misleading, but sticks around for historical reasons. You
        can choose to do a simple calculation instead, which excludes the Segment
        History from the calculation process. If there's an active attempt, you can
        choose to take it into account as well. Can return None.
        """
        if run.ptr == None:
            raise Exception("run is disposed")
        result = TimeSpan(livesplit_core_native.Analysis_calculate_sum_of_best(run.ptr, simple_calculation, use_current_run, method))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def calculate_total_playtime_for_run(run):
        """Calculates the total playtime of the passed Run.
        """
        if run.ptr == None:
            raise Exception("run is disposed")
        result = TimeSpan(livesplit_core_native.Analysis_calculate_total_playtime_for_run(run.ptr))
        return result

    @staticmethod
    def calculate_total_playtime_for_timer(timer):
        """Calculates the total playtime of the passed Timer.
        """
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = TimeSpan(livesplit_core_native.Analysis_calculate_total_playtime_for_timer(timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class AtomicDateTimeRef:
    """An Atomic Date Time represents a UTC Date Time that tries to be as close to
    an atomic clock as possible.
    """

    def is_synchronized(self):
        """Represents whether the date time is actually properly derived from an
        atomic clock. If the synchronization with the atomic clock didn't happen
        yet or failed, this is set to False.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.AtomicDateTime_is_synchronized(self.ptr)
        return result

    def to_rfc3339(self):
        """Converts this atomic date time into a RFC 3339 formatted date time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.AtomicDateTime_to_rfc3339(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class AtomicDateTimeRefMut(AtomicDateTimeRef):
    """An Atomic Date Time represents a UTC Date Time that tries to be as close to
    an atomic clock as possible.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class AtomicDateTime(AtomicDateTimeRefMut):
    """An Atomic Date Time represents a UTC Date Time that tries to be as close to
    an atomic clock as possible.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.AtomicDateTime_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class AttemptRef:
    """An Attempt describes information about an attempt to run a specific category
    by a specific runner in the past. Every time a new attempt is started and
    then reset, an Attempt describing general information about it is created.
    """

    def index(self):
        """Accesses the unique index of the attempt. This index is unique for the
        Run, not for all of them.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Attempt_index(self.ptr)
        return result

    def time(self):
        """Accesses the split time of the last segment. If the attempt got reset
        early and didn't finish, this may be empty.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.Attempt_time(self.ptr))
        return result

    def pause_time(self):
        """Accesses the amount of time the attempt has been paused for. If it is not
        known, this returns None. This means that it may not necessarily be
        possible to differentiate whether a Run has not been paused or it simply
        wasn't stored.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Attempt_pause_time(self.ptr))
        if result.ptr == None:
            return None
        return result

    def started(self):
        """Accesses the point in time the attempt was started at. This returns None
        if this information is not known.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = AtomicDateTime(livesplit_core_native.Attempt_started(self.ptr))
        if result.ptr == None:
            return None
        return result

    def ended(self):
        """Accesses the point in time the attempt was ended at. This returns None if
        this information is not known.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = AtomicDateTime(livesplit_core_native.Attempt_ended(self.ptr))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class AttemptRefMut(AttemptRef):
    """An Attempt describes information about an attempt to run a specific category
    by a specific runner in the past. Every time a new attempt is started and
    then reset, an Attempt describing general information about it is created.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class Attempt(AttemptRefMut):
    """An Attempt describes information about an attempt to run a specific category
    by a specific runner in the past. Every time a new attempt is started and
    then reset, an Attempt describing general information about it is created.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class AutoSplittingRuntimeRef:
    """With an Auto Splitting Runtime, the runner can use an Auto Splitter to
    automatically control the timer on systems that are supported.
    """

    def load_script(self, path):
        """Attempts to load an auto splitter. Returns true if successful.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.AutoSplittingRuntime_load_script(self.ptr, path.encode())
        return result

    def unload_script(self):
        """Attempts to unload the auto splitter. Returns true if successful.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.AutoSplittingRuntime_unload_script(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class AutoSplittingRuntimeRefMut(AutoSplittingRuntimeRef):
    """With an Auto Splitting Runtime, the runner can use an Auto Splitter to
    automatically control the timer on systems that are supported.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class AutoSplittingRuntime(AutoSplittingRuntimeRefMut):
    """With an Auto Splitting Runtime, the runner can use an Auto Splitter to
    automatically control the timer on systems that are supported.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.AutoSplittingRuntime_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(shared_timer):
        """Creates a new Auto Splitting Runtime for a Timer.
        """
        if shared_timer.ptr == None:
            raise Exception("shared_timer is disposed")
        result = AutoSplittingRuntime(livesplit_core_native.AutoSplittingRuntime_new(shared_timer.ptr))
        shared_timer.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponentRef:
    """The Blank Space Component is simply an empty component that doesn't show
    anything other than a background. It mostly serves as padding between other
    components.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponentRefMut(BlankSpaceComponentRef):
    """The Blank Space Component is simply an empty component that doesn't show
    anything other than a background. It mostly serves as padding between other
    components.
    """

    def state_as_json(self):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.BlankSpaceComponent_state_as_json(self.ptr)
        return result

    def state(self):
        """Calculates the component's state.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = BlankSpaceComponentState(livesplit_core_native.BlankSpaceComponent_state(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponent(BlankSpaceComponentRefMut):
    """The Blank Space Component is simply an empty component that doesn't show
    anything other than a background. It mostly serves as padding between other
    components.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.BlankSpaceComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Blank Space Component.
        """
        result = BlankSpaceComponent(livesplit_core_native.BlankSpaceComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.BlankSpaceComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def size(self):
        """The size of the component.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.BlankSpaceComponentState_size(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponentStateRefMut(BlankSpaceComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class BlankSpaceComponentState(BlankSpaceComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.BlankSpaceComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class ComponentRef:
    """A Component provides information about a run in a way that is easy to
    visualize. This type can store any of the components provided by this crate.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class ComponentRefMut(ComponentRef):
    """A Component provides information about a run in a way that is easy to
    visualize. This type can store any of the components provided by this crate.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class Component(ComponentRefMut):
    """A Component provides information about a run in a way that is easy to
    visualize. This type can store any of the components provided by this crate.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Component_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentComparisonComponentRef:
    """The Current Comparison Component is a component that shows the name of the
    comparison that is currently selected to be compared against.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentComparisonComponentRefMut(CurrentComparisonComponentRef):
    """The Current Comparison Component is a component that shows the name of the
    comparison that is currently selected to be compared against.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.CurrentComparisonComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.CurrentComparisonComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentComparisonComponent(CurrentComparisonComponentRefMut):
    """The Current Comparison Component is a component that shows the name of the
    comparison that is currently selected to be compared against.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.CurrentComparisonComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Current Comparison Component.
        """
        result = CurrentComparisonComponent(livesplit_core_native.CurrentComparisonComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.CurrentComparisonComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentPaceComponentRef:
    """The Current Pace Component is a component that shows a prediction of the
    current attempt's final time, if the current attempt's pace matches the
    chosen comparison for the remainder of the run.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentPaceComponentRefMut(CurrentPaceComponentRef):
    """The Current Pace Component is a component that shows a prediction of the
    current attempt's final time, if the current attempt's pace matches the
    chosen comparison for the remainder of the run.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.CurrentPaceComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.CurrentPaceComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class CurrentPaceComponent(CurrentPaceComponentRefMut):
    """The Current Pace Component is a component that shows a prediction of the
    current attempt's final time, if the current attempt's pace matches the
    chosen comparison for the remainder of the run.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.CurrentPaceComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Current Pace Component.
        """
        result = CurrentPaceComponent(livesplit_core_native.CurrentPaceComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.CurrentPaceComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DeltaComponentRef:
    """The Delta Component is a component that shows the how far ahead or behind
    the current attempt is compared to the chosen comparison.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class DeltaComponentRefMut(DeltaComponentRef):
    """The Delta Component is a component that shows the how far ahead or behind
    the current attempt is compared to the chosen comparison.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.DeltaComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and the layout
        settings provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = KeyValueComponentState(livesplit_core_native.DeltaComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DeltaComponent(DeltaComponentRefMut):
    """The Delta Component is a component that shows the how far ahead or behind
    the current attempt is compared to the chosen comparison.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.DeltaComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Delta Component.
        """
        result = DeltaComponent(livesplit_core_native.DeltaComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.DeltaComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponentRef:
    """The Detailed Timer Component is a component that shows two timers, one for
    the total time of the current attempt and one showing the time of just the
    current segment. Other information, like segment times of up to two
    comparisons, the segment icon, and the segment's name, can also be shown.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponentRefMut(DetailedTimerComponentRef):
    """The Detailed Timer Component is a component that shows two timers, one for
    the total time of the current attempt and one showing the time of just the
    current segment. Other information, like segment times of up to two
    comparisons, the segment icon, and the segment's name, can also be shown.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.DetailedTimerComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and layout settings
        provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = DetailedTimerComponentState(livesplit_core_native.DetailedTimerComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponent(DetailedTimerComponentRefMut):
    """The Detailed Timer Component is a component that shows two timers, one for
    the total time of the current attempt and one showing the time of just the
    current segment. Other information, like segment times of up to two
    comparisons, the segment icon, and the segment's name, can also be shown.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.DetailedTimerComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Detailed Timer Component.
        """
        result = DetailedTimerComponent(livesplit_core_native.DetailedTimerComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.DetailedTimerComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def timer_time(self):
        """The time shown by the component's main timer without the fractional part.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_timer_time(self.ptr).decode()
        return result

    def timer_fraction(self):
        """The fractional part of the time shown by the main timer (including the dot).
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_timer_fraction(self.ptr).decode()
        return result

    def timer_semantic_color(self):
        """The semantic coloring information the main timer's time carries.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_timer_semantic_color(self.ptr).decode()
        return result

    def segment_timer_time(self):
        """The time shown by the component's segment timer without the fractional part.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_segment_timer_time(self.ptr).decode()
        return result

    def segment_timer_fraction(self):
        """The fractional part of the time shown by the segment timer (including the
        dot).
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_segment_timer_fraction(self.ptr).decode()
        return result

    def comparison1_visible(self):
        """Returns whether the first comparison is visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison1_visible(self.ptr)
        return result

    def comparison1_name(self):
        """Returns the name of the first comparison. You may not call this if the first
        comparison is not visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison1_name(self.ptr).decode()
        return result

    def comparison1_time(self):
        """Returns the time of the first comparison. You may not call this if the first
        comparison is not visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison1_time(self.ptr).decode()
        return result

    def comparison2_visible(self):
        """Returns whether the second comparison is visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison2_visible(self.ptr)
        return result

    def comparison2_name(self):
        """Returns the name of the second comparison. You may not call this if the
        second comparison is not visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison2_name(self.ptr).decode()
        return result

    def comparison2_time(self):
        """Returns the time of the second comparison. You may not call this if the
        second comparison is not visible.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_comparison2_time(self.ptr).decode()
        return result

    def icon_change_ptr(self):
        """The data of the segment's icon. This value is only specified whenever the
        icon changes. If you explicitly want to query this value, remount the
        component. The buffer itself may be empty. This indicates that there is no
        icon.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_icon_change_ptr(self.ptr)
        return result

    def icon_change_len(self):
        """The length of the data of the segment's icon.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_icon_change_len(self.ptr)
        return result

    def segment_name(self):
        """The name of the segment. This may be None if it's not supposed to be
        visualized.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.DetailedTimerComponentState_segment_name(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponentStateRefMut(DetailedTimerComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class DetailedTimerComponentState(DetailedTimerComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.DetailedTimerComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class FuzzyListRef:
    """With a Fuzzy List, you can implement a fuzzy searching algorithm. The list
    stores all the items that can be searched for. With the `search` method you
    can then execute the actual fuzzy search which returns a list of all the
    elements found. This can be used to implement searching in a list of games.
    """

    def search(self, pattern, max):
        """Searches for the pattern provided in the list. A list of all the
        matching elements is returned. The returned list has a maximum amount of
        elements provided to this method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.FuzzyList_search(self.ptr, pattern.encode(), max)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class FuzzyListRefMut(FuzzyListRef):
    """With a Fuzzy List, you can implement a fuzzy searching algorithm. The list
    stores all the items that can be searched for. With the `search` method you
    can then execute the actual fuzzy search which returns a list of all the
    elements found. This can be used to implement searching in a list of games.
    """

    def push(self, text):
        """Adds a new element to the list.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.FuzzyList_push(self.ptr, text.encode())

    def __init__(self, ptr):
        self.ptr = ptr

class FuzzyList(FuzzyListRefMut):
    """With a Fuzzy List, you can implement a fuzzy searching algorithm. The list
    stores all the items that can be searched for. With the `search` method you
    can then execute the actual fuzzy search which returns a list of all the
    elements found. This can be used to implement searching in a list of games.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.FuzzyList_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Fuzzy List.
        """
        result = FuzzyList(livesplit_core_native.FuzzyList_new())
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class GeneralLayoutSettingsRef:
    """The general settings of the layout that apply to all components.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class GeneralLayoutSettingsRefMut(GeneralLayoutSettingsRef):
    """The general settings of the layout that apply to all components.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class GeneralLayoutSettings(GeneralLayoutSettingsRefMut):
    """The general settings of the layout that apply to all components.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.GeneralLayoutSettings_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def default():
        """Creates a default general layout settings configuration.
        """
        result = GeneralLayoutSettings(livesplit_core_native.GeneralLayoutSettings_default())
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponentRef:
    """The Graph Component visualizes how far the current attempt has been ahead or
    behind the chosen comparison throughout the whole attempt. All the
    individual deltas are shown as points in a graph.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.GraphComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and layout settings
        provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = GraphComponentState(livesplit_core_native.GraphComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponentRefMut(GraphComponentRef):
    """The Graph Component visualizes how far the current attempt has been ahead or
    behind the chosen comparison throughout the whole attempt. All the
    individual deltas are shown as points in a graph.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponent(GraphComponentRefMut):
    """The Graph Component visualizes how far the current attempt has been ahead or
    behind the chosen comparison throughout the whole attempt. All the
    individual deltas are shown as points in a graph.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.GraphComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Graph Component.
        """
        result = GraphComponent(livesplit_core_native.GraphComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.GraphComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponentStateRef:
    """The state object describes the information to visualize for this component.
    All the coordinates are in the range 0..1.
    """

    def points_len(self):
        """Returns the amount of points to visualize. Connect all of them to visualize
        the graph. If the live delta is active, the last point is to be interpreted
        as a preview of the next split that is about to happen. Use the partial fill
        color to visualize the region beneath that graph segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_points_len(self.ptr)
        return result

    def point_x(self, index):
        """Returns the x coordinate of the point specified. You may not provide an out
        of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_point_x(self.ptr, index)
        return result

    def point_y(self, index):
        """Returns the y coordinate of the point specified. You may not provide an out
        of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_point_y(self.ptr, index)
        return result

    def point_is_best_segment(self, index):
        """Describes whether the segment the point specified is visualizing achieved a
        new best segment time. Use the best segment color for it, in that case. You
        may not provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_point_is_best_segment(self.ptr, index)
        return result

    def horizontal_grid_lines_len(self):
        """Describes how many horizontal grid lines to visualize.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_horizontal_grid_lines_len(self.ptr)
        return result

    def horizontal_grid_line(self, index):
        """Accesses the y coordinate of the horizontal grid line specified. You may not
        provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_horizontal_grid_line(self.ptr, index)
        return result

    def vertical_grid_lines_len(self):
        """Describes how many vertical grid lines to visualize.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_vertical_grid_lines_len(self.ptr)
        return result

    def vertical_grid_line(self, index):
        """Accesses the x coordinate of the vertical grid line specified. You may not
        provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_vertical_grid_line(self.ptr, index)
        return result

    def middle(self):
        """The y coordinate that separates the region that shows the times that are
        ahead of the comparison and those that are behind.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_middle(self.ptr)
        return result

    def is_live_delta_active(self):
        """If the live delta is active, the last point is to be interpreted as a
        preview of the next split that is about to happen. Use the partial fill
        color to visualize the region beneath that graph segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_is_live_delta_active(self.ptr)
        return result

    def is_flipped(self):
        """Describes whether the graph is flipped vertically. For visualizing the
        graph, this usually doesn't need to be interpreted, as this information is
        entirely encoded into the other variables.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.GraphComponentState_is_flipped(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponentStateRefMut(GraphComponentStateRef):
    """The state object describes the information to visualize for this component.
    All the coordinates are in the range 0..1.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class GraphComponentState(GraphComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    All the coordinates are in the range 0..1.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.GraphComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeyConfigRef:
    """The configuration to use for a Hotkey System. It describes with keys to use
    as hotkeys for the different actions.
    """

    def settings_description_as_json(self):
        """Encodes generic description of the settings available for the hotkey
        configuration and their current values as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.HotkeyConfig_settings_description_as_json(self.ptr)
        return result

    def as_json(self):
        """Encodes the hotkey configuration as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.HotkeyConfig_as_json(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeyConfigRefMut(HotkeyConfigRef):
    """The configuration to use for a Hotkey System. It describes with keys to use
    as hotkeys for the different actions.
    """

    def set_value(self, index, value):
        """Sets a setting's value by its index to the given value.
        
        False is returned if a hotkey is already in use by a different action.
        
        This panics if the type of the value to be set is not compatible with the
        type of the setting's value. A panic can also occur if the index of the
        setting provided is out of bounds.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if value.ptr == None:
            raise Exception("value is disposed")
        result = livesplit_core_native.HotkeyConfig_set_value(self.ptr, index, value.ptr)
        value.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeyConfig(HotkeyConfigRefMut):
    """The configuration to use for a Hotkey System. It describes with keys to use
    as hotkeys for the different actions.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.HotkeyConfig_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Hotkey Configuration with default settings.
        """
        result = HotkeyConfig(livesplit_core_native.HotkeyConfig_new())
        return result

    @staticmethod
    def parse_json(settings):
        """Parses a hotkey configuration from the given JSON description. None is
        returned if it couldn't be parsed.
        """
        result = HotkeyConfig(livesplit_core_native.HotkeyConfig_parse_json(settings))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def parse_file_handle(handle):
        """Attempts to parse a hotkey configuration from a given file. None is
        returned it couldn't be parsed. This will not close the file descriptor /
        handle.
        """
        result = HotkeyConfig(livesplit_core_native.HotkeyConfig_parse_file_handle(handle))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeySystemRef:
    """With a Hotkey System the runner can use hotkeys on their keyboard to control
    the Timer. The hotkeys are global, so the application doesn't need to be in
    focus. The behavior of the hotkeys depends on the platform and is stubbed
    out on platforms that don't support hotkeys. You can turn off a Hotkey
    System temporarily. By default the Hotkey System is activated.
    """

    def config(self):
        """Returns the hotkey configuration currently in use by the Hotkey System.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = HotkeyConfig(livesplit_core_native.HotkeySystem_config(self.ptr))
        return result

    def resolve(self, key_code):
        """Resolves the key according to the current keyboard layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.HotkeySystem_resolve(self.ptr, key_code.encode()).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeySystemRefMut(HotkeySystemRef):
    """With a Hotkey System the runner can use hotkeys on their keyboard to control
    the Timer. The hotkeys are global, so the application doesn't need to be in
    focus. The behavior of the hotkeys depends on the platform and is stubbed
    out on platforms that don't support hotkeys. You can turn off a Hotkey
    System temporarily. By default the Hotkey System is activated.
    """

    def deactivate(self):
        """Deactivates the Hotkey System. No hotkeys will go through until it gets
        activated again. If it's already deactivated, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.HotkeySystem_deactivate(self.ptr)
        return result

    def activate(self):
        """Activates a previously deactivated Hotkey System. If it's already
        active, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.HotkeySystem_activate(self.ptr)
        return result

    def set_config(self, config):
        """Applies a new hotkey configuration to the Hotkey System. Each hotkey is
        changed to the one specified in the configuration. This operation may fail
        if you provide a hotkey configuration where a hotkey is used for multiple
        operations. Returns False if the operation failed.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if config.ptr == None:
            raise Exception("config is disposed")
        result = livesplit_core_native.HotkeySystem_set_config(self.ptr, config.ptr)
        config.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class HotkeySystem(HotkeySystemRefMut):
    """With a Hotkey System the runner can use hotkeys on their keyboard to control
    the Timer. The hotkeys are global, so the application doesn't need to be in
    focus. The behavior of the hotkeys depends on the platform and is stubbed
    out on platforms that don't support hotkeys. You can turn off a Hotkey
    System temporarily. By default the Hotkey System is activated.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.HotkeySystem_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(shared_timer):
        """Creates a new Hotkey System for a Timer with the default hotkeys.
        """
        if shared_timer.ptr == None:
            raise Exception("shared_timer is disposed")
        result = HotkeySystem(livesplit_core_native.HotkeySystem_new(shared_timer.ptr))
        shared_timer.ptr = None
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def with_config(shared_timer, config):
        """Creates a new Hotkey System for a Timer with a custom configuration for the
        hotkeys.
        """
        if shared_timer.ptr == None:
            raise Exception("shared_timer is disposed")
        if config.ptr == None:
            raise Exception("config is disposed")
        result = HotkeySystem(livesplit_core_native.HotkeySystem_with_config(shared_timer.ptr, config.ptr))
        shared_timer.ptr = None
        config.ptr = None
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class KeyValueComponentStateRef:
    """The state object describes the information to visualize for a key value based component.
    """

    def key(self):
        """The key to visualize.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.KeyValueComponentState_key(self.ptr).decode()
        return result

    def value(self):
        """The value to visualize.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.KeyValueComponentState_value(self.ptr).decode()
        return result

    def semantic_color(self):
        """The semantic coloring information the value carries.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.KeyValueComponentState_semantic_color(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class KeyValueComponentStateRefMut(KeyValueComponentStateRef):
    """The state object describes the information to visualize for a key value based component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class KeyValueComponentState(KeyValueComponentStateRefMut):
    """The state object describes the information to visualize for a key value based component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.KeyValueComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutRef:
    """A Layout allows you to combine multiple components together to visualize a
    variety of information the runner is interested in.
    """

    def clone(self):
        """Clones the layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Layout(livesplit_core_native.Layout_clone(self.ptr))
        return result

    def settings_as_json(self):
        """Encodes the settings of the layout as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Layout_settings_as_json(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutRefMut(LayoutRef):
    """A Layout allows you to combine multiple components together to visualize a
    variety of information the runner is interested in.
    """

    def state(self, timer):
        """Calculates and returns the layout's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = LayoutState(livesplit_core_native.Layout_state(self.ptr, timer.ptr))
        return result

    def update_state(self, state, timer):
        """Updates the layout's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if state.ptr == None:
            raise Exception("state is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        livesplit_core_native.Layout_update_state(self.ptr, state.ptr, timer.ptr)

    def update_state_as_json(self, state, timer):
        """Updates the layout's state based on the timer provided and encodes it as
        JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if state.ptr == None:
            raise Exception("state is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.Layout_update_state_as_json(self.ptr, state.ptr, timer.ptr)
        return result

    def state_as_json(self, timer):
        """Calculates the layout's state based on the timer provided and encodes it as
        JSON. You can use this to visualize all of the components of a layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.Layout_state_as_json(self.ptr, timer.ptr)
        return result

    def push(self, component):
        """Adds a new component to the end of the layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if component.ptr == None:
            raise Exception("component is disposed")
        livesplit_core_native.Layout_push(self.ptr, component.ptr)
        component.ptr = None

    def scroll_up(self):
        """Scrolls up all the components in the layout that can be scrolled up.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Layout_scroll_up(self.ptr)

    def scroll_down(self):
        """Scrolls down all the components in the layout that can be scrolled down.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Layout_scroll_down(self.ptr)

    def remount(self):
        """Remounts all the components as if they were freshly initialized. Some
        components may only provide some information whenever it changes or when
        their state is first queried. Remounting returns this information again,
        whenever the layout's state is queried the next time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Layout_remount(self.ptr)

    def __init__(self, ptr):
        self.ptr = ptr

class Layout(LayoutRefMut):
    """A Layout allows you to combine multiple components together to visualize a
    variety of information the runner is interested in.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Layout_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new empty layout with no components.
        """
        result = Layout(livesplit_core_native.Layout_new())
        return result

    @staticmethod
    def default_layout():
        """Creates a new default layout that contains a default set of components
        in order to provide a good default layout for runners. Which components
        are provided by this and how they are configured may change in the
        future.
        """
        result = Layout(livesplit_core_native.Layout_default_layout())
        return result

    @staticmethod
    def parse_json(settings):
        """Parses a layout from the given JSON description of its settings. None is
        returned if it couldn't be parsed.
        """
        result = Layout(livesplit_core_native.Layout_parse_json(settings))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def parse_file_handle(handle):
        """Attempts to parse a layout from a given file. None is returned it couldn't
        be parsed. This will not close the file descriptor / handle.
        """
        result = Layout(livesplit_core_native.Layout_parse_file_handle(handle))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def parse_original_livesplit(data, length):
        """Parses a layout saved by the original LiveSplit. This is lossy, as not
        everything can be converted completely. None is returned if it couldn't be
        parsed at all.
        """
        result = Layout(livesplit_core_native.Layout_parse_original_livesplit(data, length))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditorRef:
    """The Layout Editor allows modifying Layouts while ensuring all the different
    invariants of the Layout objects are upheld no matter what kind of
    operations are being applied. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def state_as_json(self):
        """Encodes the Layout Editor's state as JSON in order to visualize it.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditor_state_as_json(self.ptr)
        return result

    def state(self):
        """Returns the state of the Layout Editor.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = LayoutEditorState(livesplit_core_native.LayoutEditor_state(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditorRefMut(LayoutEditorRef):
    """The Layout Editor allows modifying Layouts while ensuring all the different
    invariants of the Layout objects are upheld no matter what kind of
    operations are being applied. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def layout_state_as_json(self, timer):
        """Encodes the layout's state as JSON based on the timer provided. You can use
        this to visualize all of the components of a layout, while it is still being
        edited by the Layout Editor.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.LayoutEditor_layout_state_as_json(self.ptr, timer.ptr)
        return result

    def update_layout_state(self, state, timer):
        """Updates the layout's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if state.ptr == None:
            raise Exception("state is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        livesplit_core_native.LayoutEditor_update_layout_state(self.ptr, state.ptr, timer.ptr)

    def update_layout_state_as_json(self, state, timer):
        """Updates the layout's state based on the timer provided and encodes it as
        JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if state.ptr == None:
            raise Exception("state is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.LayoutEditor_update_layout_state_as_json(self.ptr, state.ptr, timer.ptr)
        return result

    def select(self, index):
        """Selects the component with the given index in order to modify its
        settings. Only a single component is selected at any given time. You may
        not provide an invalid index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_select(self.ptr, index)

    def add_component(self, component):
        """Adds the component provided to the end of the layout. The newly added
        component becomes the selected component.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if component.ptr == None:
            raise Exception("component is disposed")
        livesplit_core_native.LayoutEditor_add_component(self.ptr, component.ptr)
        component.ptr = None

    def remove_component(self):
        """Removes the currently selected component, unless there's only one
        component in the layout. The next component becomes the selected
        component. If there's none, the previous component becomes the selected
        component instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_remove_component(self.ptr)

    def move_component_up(self):
        """Moves the selected component up, unless the first component is selected.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_move_component_up(self.ptr)

    def move_component_down(self):
        """Moves the selected component down, unless the last component is
        selected.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_move_component_down(self.ptr)

    def move_component(self, dst_index):
        """Moves the selected component to the index provided. You may not provide
        an invalid index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_move_component(self.ptr, dst_index)

    def duplicate_component(self):
        """Duplicates the currently selected component. The copy gets placed right
        after the selected component and becomes the newly selected component.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.LayoutEditor_duplicate_component(self.ptr)

    def set_component_settings_value(self, index, value):
        """Sets a setting's value of the selected component by its setting index
        to the given value.
        
        This panics if the type of the value to be set is not compatible with
        the type of the setting's value. A panic can also occur if the index of
        the setting provided is out of bounds.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if value.ptr == None:
            raise Exception("value is disposed")
        livesplit_core_native.LayoutEditor_set_component_settings_value(self.ptr, index, value.ptr)
        value.ptr = None

    def set_general_settings_value(self, index, value):
        """Sets a setting's value of the general settings by its setting index to
        the given value.
        
        This panics if the type of the value to be set is not compatible with
        the type of the setting's value. A panic can also occur if the index of
        the setting provided is out of bounds.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if value.ptr == None:
            raise Exception("value is disposed")
        livesplit_core_native.LayoutEditor_set_general_settings_value(self.ptr, index, value.ptr)
        value.ptr = None

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditor(LayoutEditorRefMut):
    """The Layout Editor allows modifying Layouts while ensuring all the different
    invariants of the Layout objects are upheld no matter what kind of
    operations are being applied. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(layout):
        """Creates a new Layout Editor that modifies the Layout provided. Creation of
        the Layout Editor fails when a Layout with no components is provided. In
        that case None is returned instead.
        """
        if layout.ptr == None:
            raise Exception("layout is disposed")
        result = LayoutEditor(livesplit_core_native.LayoutEditor_new(layout.ptr))
        layout.ptr = None
        if result.ptr == None:
            return None
        return result

    def close(self):
        """Closes the Layout Editor and gives back access to the modified Layout. In
        case you want to implement a Cancel Button, just dispose the Layout object
        you get here.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Layout(livesplit_core_native.LayoutEditor_close(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditorStateRef:
    """Represents the current state of the Layout Editor in order to visualize it properly.
    """

    def component_len(self):
        """Returns the number of components in the layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_component_len(self.ptr)
        return result

    def component_text(self, index):
        """Returns the name of the component at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_component_text(self.ptr, index).decode()
        return result

    def buttons(self):
        """Returns a bitfield corresponding to which buttons are active.
        
        The bits are as follows:
        
        * `0x04` - Can remove the current component
        * `0x02` - Can move the current component up
        * `0x01` - Can move the current component down
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_buttons(self.ptr)
        return result

    def selected_component(self):
        """Returns the index of the currently selected component.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_selected_component(self.ptr)
        return result

    def field_len(self, component_settings):
        """Returns the number of fields in the layout's settings.
        
        Set `component_settings` to true to use the selected component's settings instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_field_len(self.ptr, component_settings)
        return result

    def field_text(self, component_settings, index):
        """Returns the name of the layout's setting at the specified index.
        
        Set `component_settings` to true to use the selected component's settings instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutEditorState_field_text(self.ptr, component_settings, index).decode()
        return result

    def field_value(self, component_settings, index):
        """Returns the value of the layout's setting at the specified index.
        
        Set `component_settings` to true to use the selected component's settings instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SettingValueRef(livesplit_core_native.LayoutEditorState_field_value(self.ptr, component_settings, index))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditorStateRefMut(LayoutEditorStateRef):
    """Represents the current state of the Layout Editor in order to visualize it properly.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutEditorState(LayoutEditorStateRefMut):
    """Represents the current state of the Layout Editor in order to visualize it properly.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.LayoutEditorState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutStateRef:
    """The state object describes the information to visualize for an entire
    layout. Use this with care, as invalid usage will result in a panic.
    
    Specifically, you should avoid doing the following:
    
    - Using out of bounds indices.
    - Using the wrong getter function on the wrong type of component.
    """

    def as_json(self):
        """Encodes the layout state as JSON. You can use this to visualize all of the
        components of a layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutState_as_json(self.ptr)
        return result

    def len(self):
        """Gets the number of Components in the Layout State.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutState_len(self.ptr)
        return result

    def component_type(self, index):
        """Returns a string describing the type of the Component at the specified
        index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.LayoutState_component_type(self.ptr, index).decode()
        return result

    def component_as_blank_space(self, index):
        """Gets the Blank Space component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = BlankSpaceComponentStateRef(livesplit_core_native.LayoutState_component_as_blank_space(self.ptr, index))
        return result

    def component_as_detailed_timer(self, index):
        """Gets the Detailed Timer component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = DetailedTimerComponentStateRef(livesplit_core_native.LayoutState_component_as_detailed_timer(self.ptr, index))
        return result

    def component_as_graph(self, index):
        """Gets the Graph component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = GraphComponentStateRef(livesplit_core_native.LayoutState_component_as_graph(self.ptr, index))
        return result

    def component_as_key_value(self, index):
        """Gets the Key Value component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = KeyValueComponentStateRef(livesplit_core_native.LayoutState_component_as_key_value(self.ptr, index))
        return result

    def component_as_separator(self, index):
        """Gets the Separator component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SeparatorComponentStateRef(livesplit_core_native.LayoutState_component_as_separator(self.ptr, index))
        return result

    def component_as_splits(self, index):
        """Gets the Splits component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SplitsComponentStateRef(livesplit_core_native.LayoutState_component_as_splits(self.ptr, index))
        return result

    def component_as_text(self, index):
        """Gets the Text component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TextComponentStateRef(livesplit_core_native.LayoutState_component_as_text(self.ptr, index))
        return result

    def component_as_timer(self, index):
        """Gets the Timer component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimerComponentStateRef(livesplit_core_native.LayoutState_component_as_timer(self.ptr, index))
        return result

    def component_as_title(self, index):
        """Gets the Title component state at the specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TitleComponentStateRef(livesplit_core_native.LayoutState_component_as_title(self.ptr, index))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutStateRefMut(LayoutStateRef):
    """The state object describes the information to visualize for an entire
    layout. Use this with care, as invalid usage will result in a panic.
    
    Specifically, you should avoid doing the following:
    
    - Using out of bounds indices.
    - Using the wrong getter function on the wrong type of component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class LayoutState(LayoutStateRefMut):
    """The state object describes the information to visualize for an entire
    layout. Use this with care, as invalid usage will result in a panic.
    
    Specifically, you should avoid doing the following:
    
    - Using out of bounds indices.
    - Using the wrong getter function on the wrong type of component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.LayoutState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new empty Layout State. This is useful for creating an empty
        layout state that gets updated over time.
        """
        result = LayoutState(livesplit_core_native.LayoutState_new())
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class ParseRunResultRef:
    """A run parsed by the Composite Parser. This contains the Run itself and
    information about which parser parsed it.
    """

    def parsed_successfully(self):
        """Returns True if the Run got parsed successfully. False is returned otherwise.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.ParseRunResult_parsed_successfully(self.ptr)
        return result

    def timer_kind(self):
        """Accesses the name of the Parser that parsed the Run. You may not call this
        if the Run wasn't parsed successfully.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.ParseRunResult_timer_kind(self.ptr).decode()
        return result

    def is_generic_timer(self):
        """Checks whether the Parser parsed a generic timer. Since a generic timer can
        have any name, it may clash with the specific timer formats that
        livesplit-core supports. With this function you can determine if a generic
        timer format was parsed, instead of one of the more specific timer formats.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.ParseRunResult_is_generic_timer(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class ParseRunResultRefMut(ParseRunResultRef):
    """A run parsed by the Composite Parser. This contains the Run itself and
    information about which parser parsed it.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class ParseRunResult(ParseRunResultRefMut):
    """A run parsed by the Composite Parser. This contains the Run itself and
    information about which parser parsed it.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.ParseRunResult_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def unwrap(self):
        """Moves the actual Run object out of the Result. You may not call this if the
        Run wasn't parsed successfully.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Run(livesplit_core_native.ParseRunResult_unwrap(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PbChanceComponentRef:
    """The PB Chance Component is a component that shows how likely it is to beat
    the Personal Best. If there is no active attempt it shows the general chance
    of beating the Personal Best. During an attempt it actively changes based on
    how well the attempt is going.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.PbChanceComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.PbChanceComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PbChanceComponentRefMut(PbChanceComponentRef):
    """The PB Chance Component is a component that shows how likely it is to beat
    the Personal Best. If there is no active attempt it shows the general chance
    of beating the Personal Best. During an attempt it actively changes based on
    how well the attempt is going.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class PbChanceComponent(PbChanceComponentRefMut):
    """The PB Chance Component is a component that shows how likely it is to beat
    the Personal Best. If there is no active attempt it shows the general chance
    of beating the Personal Best. During an attempt it actively changes based on
    how well the attempt is going.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.PbChanceComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new PB Chance Component.
        """
        result = PbChanceComponent(livesplit_core_native.PbChanceComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.PbChanceComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PossibleTimeSaveComponentRef:
    """The Possible Time Save Component is a component that shows how much time the
    chosen comparison could've saved for the current segment, based on the Best
    Segments. This component also allows showing the Total Possible Time Save
    for the remainder of the current attempt.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.PossibleTimeSaveComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.PossibleTimeSaveComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PossibleTimeSaveComponentRefMut(PossibleTimeSaveComponentRef):
    """The Possible Time Save Component is a component that shows how much time the
    chosen comparison could've saved for the current segment, based on the Best
    Segments. This component also allows showing the Total Possible Time Save
    for the remainder of the current attempt.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class PossibleTimeSaveComponent(PossibleTimeSaveComponentRefMut):
    """The Possible Time Save Component is a component that shows how much time the
    chosen comparison could've saved for the current segment, based on the Best
    Segments. This component also allows showing the Total Possible Time Save
    for the remainder of the current attempt.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.PossibleTimeSaveComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Possible Time Save Component.
        """
        result = PossibleTimeSaveComponent(livesplit_core_native.PossibleTimeSaveComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.PossibleTimeSaveComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PotentialCleanUpRef:
    """Describes a potential clean up that could be applied. You can query a
    message describing the details of this potential clean up. A potential clean
    up can then be turned into an actual clean up in order to apply it to the
    Run.
    """

    def message(self):
        """Accesses the message describing the potential clean up that can be applied
        to a Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.PotentialCleanUp_message(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PotentialCleanUpRefMut(PotentialCleanUpRef):
    """Describes a potential clean up that could be applied. You can query a
    message describing the details of this potential clean up. A potential clean
    up can then be turned into an actual clean up in order to apply it to the
    Run.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class PotentialCleanUp(PotentialCleanUpRefMut):
    """Describes a potential clean up that could be applied. You can query a
    message describing the details of this potential clean up. A potential clean
    up can then be turned into an actual clean up in order to apply it to the
    Run.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.PotentialCleanUp_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class PreviousSegmentComponentRef:
    """The Previous Segment Component is a component that shows how much time was
    saved or lost during the previous segment based on the chosen comparison.
    Additionally, the potential time save for the previous segment can be
    displayed. This component switches to a `Live Segment` view that shows
    active time loss whenever the runner is losing time on the current segment.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.PreviousSegmentComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and the layout
        settings provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = KeyValueComponentState(livesplit_core_native.PreviousSegmentComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class PreviousSegmentComponentRefMut(PreviousSegmentComponentRef):
    """The Previous Segment Component is a component that shows how much time was
    saved or lost during the previous segment based on the chosen comparison.
    Additionally, the potential time save for the previous segment can be
    displayed. This component switches to a `Live Segment` view that shows
    active time loss whenever the runner is losing time on the current segment.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class PreviousSegmentComponent(PreviousSegmentComponentRefMut):
    """The Previous Segment Component is a component that shows how much time was
    saved or lost during the previous segment based on the chosen comparison.
    Additionally, the potential time save for the previous segment can be
    displayed. This component switches to a `Live Segment` view that shows
    active time loss whenever the runner is losing time on the current segment.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.PreviousSegmentComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Previous Segment Component.
        """
        result = PreviousSegmentComponent(livesplit_core_native.PreviousSegmentComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.PreviousSegmentComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunRef:
    """A Run stores the split times for a specific game and category of a runner.
    """

    def clone(self):
        """Clones the Run object.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Run(livesplit_core_native.Run_clone(self.ptr))
        return result

    def game_name(self):
        """Accesses the name of the game this Run is for.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_game_name(self.ptr).decode()
        return result

    def game_icon_ptr(self):
        """Accesses the game icon's data. If there is no game icon, this returns an
        empty buffer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_game_icon_ptr(self.ptr)
        return result

    def game_icon_len(self):
        """Accesses the amount of bytes the game icon's data takes up.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_game_icon_len(self.ptr)
        return result

    def category_name(self):
        """Accesses the name of the category this Run is for.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_category_name(self.ptr).decode()
        return result

    def extended_file_name(self, use_extended_category_name):
        """Returns a file name (without the extension) suitable for this Run that
        is built the following way:
        
        Game Name - Category Name
        
        If either is empty, the dash is omitted. Special characters that cause
        problems in file names are also omitted. If an extended category name is
        used, the variables of the category are appended in a parenthesis.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_extended_file_name(self.ptr, use_extended_category_name).decode()
        return result

    def extended_name(self, use_extended_category_name):
        """Returns a name suitable for this Run that is built the following way:
        
        Game Name - Category Name
        
        If either is empty, the dash is omitted. If an extended category name is
        used, the variables of the category are appended in a parenthesis.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_extended_name(self.ptr, use_extended_category_name).decode()
        return result

    def extended_category_name(self, show_region, show_platform, show_variables):
        """Returns an extended category name that possibly includes the region,
        platform and variables, depending on the arguments provided. An extended
        category name may look like this:
        
        Any% (No Tuner, JPN, Wii Emulator)
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_extended_category_name(self.ptr, show_region, show_platform, show_variables).decode()
        return result

    def attempt_count(self):
        """Returns the amount of runs that have been attempted with these splits.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_attempt_count(self.ptr)
        return result

    def metadata(self):
        """Accesses additional metadata of this Run, like the platform and region
        of the game.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunMetadataRef(livesplit_core_native.Run_metadata(self.ptr))
        return result

    def offset(self):
        """Accesses the time an attempt of this Run should start at.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Run_offset(self.ptr))
        return result

    def len(self):
        """Returns the amount of segments stored in this Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_len(self.ptr)
        return result

    def has_been_modified(self):
        """Returns whether the Run has been modified and should be saved so that the
        changes don't get lost.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_has_been_modified(self.ptr)
        return result

    def segment(self, index):
        """Accesses a certain segment of this Run. You may not provide an out of bounds
        index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SegmentRef(livesplit_core_native.Run_segment(self.ptr, index))
        return result

    def attempt_history_len(self):
        """Returns the amount attempt history elements are stored in this Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_attempt_history_len(self.ptr)
        return result

    def attempt_history_index(self, index):
        """Accesses the an attempt history element by its index. This does not store
        the actual segment times, just the overall attempt information. Information
        about the individual segments is stored within each segment. You may not
        provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = AttemptRef(livesplit_core_native.Run_attempt_history_index(self.ptr, index))
        return result

    def save_as_lss(self):
        """Saves a Run as a LiveSplit splits file (*.lss). If the run is actively in
        use by a timer, use the appropriate method on the timer instead, in order to
        properly save the current attempt as well.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_save_as_lss(self.ptr).decode()
        return result

    def custom_comparisons_len(self):
        """Returns the amount of custom comparisons stored in this Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_custom_comparisons_len(self.ptr)
        return result

    def custom_comparison(self, index):
        """Accesses a custom comparison stored in this Run by its index. This includes
        `Personal Best` but excludes all the other Comparison Generators. You may
        not provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_custom_comparison(self.ptr, index).decode()
        return result

    def auto_splitter_settings(self):
        """Accesses the Auto Splitter Settings that are encoded as XML.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Run_auto_splitter_settings(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunRefMut(RunRef):
    """A Run stores the split times for a specific game and category of a runner.
    """

    def push_segment(self, segment):
        """Pushes the segment provided to the end of the list of segments of this Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if segment.ptr == None:
            raise Exception("segment is disposed")
        livesplit_core_native.Run_push_segment(self.ptr, segment.ptr)
        segment.ptr = None

    def set_game_name(self, game):
        """Sets the name of the game this Run is for.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Run_set_game_name(self.ptr, game.encode())

    def set_category_name(self, category):
        """Sets the name of the category this Run is for.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Run_set_category_name(self.ptr, category.encode())

    def mark_as_modified(self):
        """Marks the Run as modified, so that it is known that there are changes
        that should be saved.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Run_mark_as_modified(self.ptr)

    def __init__(self, ptr):
        self.ptr = ptr

class Run(RunRefMut):
    """A Run stores the split times for a specific game and category of a runner.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Run_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Run object with no segments.
        """
        result = Run(livesplit_core_native.Run_new())
        return result

    @staticmethod
    def parse(data, length, load_files_path):
        """Attempts to parse a splits file from an array by invoking the corresponding
        parser for the file format detected. Additionally you can provide the path
        of the splits file so additional files, like external images, can be loaded.
        If you are using livesplit-core in a server-like environment, set this to
        None. Only client-side applications should provide a path here. Unlike the
        normal parsing function, it also fixes problems in the Run, such as
        decreasing times and missing information.
        """
        result = ParseRunResult(livesplit_core_native.Run_parse(data, length, load_files_path.encode()))
        return result

    @staticmethod
    def parse_file_handle(handle, load_files_path):
        """Attempts to parse a splits file from a file by invoking the corresponding
        parser for the file format detected. Additionally you can provide the path
        of the splits file so additional files, like external images, can be loaded.
        If you are using livesplit-core in a server-like environment, set this to
        None. Only client-side applications should provide a path here. Unlike the
        normal parsing function, it also fixes problems in the Run, such as
        decreasing times and missing information. On Unix you pass a file descriptor
        to this function. On Windows you pass a file handle to this function. The
        file descriptor / handle does not get closed.
        """
        result = ParseRunResult(livesplit_core_native.Run_parse_file_handle(handle, load_files_path.encode()))
        return result

    @staticmethod
    def parse_file(file, load_files_path):
        data = file.read()
        if sys.version_info[0] > 2:
            if isinstance(data, str):
                raise TypeError("File must be opened in binary mode!")
        bytes = bytearray(data)
        bufferType = c_byte * len(bytes)
        buffer = bufferType(*bytes)
        return Run.parse(buffer, len(bytes), load_files_path)

    def __init__(self, ptr):
        self.ptr = ptr

class RunEditorRef:
    """The Run Editor allows modifying Runs while ensuring that all the different
    invariants of the Run objects are upheld no matter what kind of operations
    are being applied to the Run. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunEditorRefMut(RunEditorRef):
    """The Run Editor allows modifying Runs while ensuring that all the different
    invariants of the Run objects are upheld no matter what kind of operations
    are being applied to the Run. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def state_as_json(self):
        """Calculates the Run Editor's state and encodes it as
        JSON in order to visualize it.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_state_as_json(self.ptr)
        return result

    def select_timing_method(self, method):
        """Selects a different timing method for being modified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_select_timing_method(self.ptr, method)

    def unselect(self, index):
        """Unselects the segment with the given index. If it's not selected or the
        index is out of bounds, nothing happens. The segment is not unselected,
        when it is the only segment that is selected. If the active segment is
        unselected, the most recently selected segment remaining becomes the
        active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_unselect(self.ptr, index)

    def select_additionally(self, index):
        """In addition to the segments that are already selected, the segment with
        the given index is being selected. The segment chosen also becomes the
        active segment.
        
        This panics if the index of the segment provided is out of bounds.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_select_additionally(self.ptr, index)

    def select_only(self, index):
        """Selects the segment with the given index. All other segments are
        unselected. The segment chosen also becomes the active segment.
        
        This panics if the index of the segment provided is out of bounds.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_select_only(self.ptr, index)

    def set_game_name(self, game):
        """Sets the name of the game.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_game_name(self.ptr, game.encode())

    def set_category_name(self, category):
        """Sets the name of the category.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_category_name(self.ptr, category.encode())

    def parse_and_set_offset(self, offset):
        """Parses and sets the timer offset from the string provided. The timer
        offset specifies the time, the timer starts at when starting a new
        attempt.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_parse_and_set_offset(self.ptr, offset.encode())
        return result

    def parse_and_set_attempt_count(self, attempts):
        """Parses and sets the attempt count from the string provided. Changing
        this has no affect on the attempt history or the segment history. This
        number is mostly just a visual number for the runner.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_parse_and_set_attempt_count(self.ptr, attempts.encode())
        return result

    def set_game_icon(self, data, length):
        """Sets the game's icon.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_game_icon(self.ptr, data, length)

    def remove_game_icon(self):
        """Removes the game's icon.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_remove_game_icon(self.ptr)

    def set_run_id(self, name):
        """Sets the speedrun.com Run ID of the run. You need to ensure that the
        record on speedrun.com matches up with the Personal Best of this run.
        This may be empty if there's no association.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_run_id(self.ptr, name.encode())

    def set_region_name(self, name):
        """Sets the name of the region this game is from. This may be empty if it's
        not specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_region_name(self.ptr, name.encode())

    def set_platform_name(self, name):
        """Sets the name of the platform this game is run on. This may be empty if
        it's not specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_platform_name(self.ptr, name.encode())

    def set_emulator_usage(self, uses_emulator):
        """Specifies whether this speedrun is done on an emulator. Keep in mind
        that False may also mean that this information is simply not known.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_emulator_usage(self.ptr, uses_emulator)

    def set_speedrun_com_variable(self, name, value):
        """Sets the speedrun.com variable with the name specified to the value specified. A
        variable is an arbitrary key value pair storing additional information
        about the category. An example of this may be whether Amiibos are used
        in this category. If the variable doesn't exist yet, it is being
        inserted.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_speedrun_com_variable(self.ptr, name.encode(), value.encode())

    def remove_speedrun_com_variable(self, name):
        """Removes the speedrun.com variable with the name specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_remove_speedrun_com_variable(self.ptr, name.encode())

    def add_custom_variable(self, name):
        """Adds a new permanent custom variable. If there's a temporary variable with
        the same name, it gets turned into a permanent variable and its value stays.
        If a permanent variable with the name already exists, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_add_custom_variable(self.ptr, name.encode())

    def set_custom_variable(self, name, value):
        """Sets the value of a custom variable with the name specified. If the custom
        variable does not exist, or is not a permanent variable, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_set_custom_variable(self.ptr, name.encode(), value.encode())

    def remove_custom_variable(self, name):
        """Removes the custom variable with the name specified. If the custom variable
        does not exist, or is not a permanent variable, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_remove_custom_variable(self.ptr, name.encode())

    def clear_metadata(self):
        """Resets all the Metadata Information.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_clear_metadata(self.ptr)

    def insert_segment_above(self):
        """Inserts a new empty segment above the active segment and adjusts the
        Run's history information accordingly. The newly created segment is then
        the only selected segment and also the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_insert_segment_above(self.ptr)

    def insert_segment_below(self):
        """Inserts a new empty segment below the active segment and adjusts the
        Run's history information accordingly. The newly created segment is then
        the only selected segment and also the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_insert_segment_below(self.ptr)

    def remove_segments(self):
        """Removes all the selected segments, unless all of them are selected. The
        run's information is automatically adjusted properly. The next
        not-to-be-removed segment after the active segment becomes the new
        active segment. If there's none, then the next not-to-be-removed segment
        before the active segment, becomes the new active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_remove_segments(self.ptr)

    def move_segments_up(self):
        """Moves all the selected segments up, unless the first segment is
        selected. The run's information is automatically adjusted properly. The
        active segment stays the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_move_segments_up(self.ptr)

    def move_segments_down(self):
        """Moves all the selected segments down, unless the last segment is
        selected. The run's information is automatically adjusted properly. The
        active segment stays the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_move_segments_down(self.ptr)

    def active_set_icon(self, data, length):
        """Sets the icon of the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_active_set_icon(self.ptr, data, length)

    def active_remove_icon(self):
        """Removes the icon of the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_active_remove_icon(self.ptr)

    def active_set_name(self, name):
        """Sets the name of the active segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_active_set_name(self.ptr, name.encode())

    def active_parse_and_set_split_time(self, time):
        """Parses a split time from a string and sets it for the active segment with
        the chosen timing method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_active_parse_and_set_split_time(self.ptr, time.encode())
        return result

    def active_parse_and_set_segment_time(self, time):
        """Parses a segment time from a string and sets it for the active segment with
        the chosen timing method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_active_parse_and_set_segment_time(self.ptr, time.encode())
        return result

    def active_parse_and_set_best_segment_time(self, time):
        """Parses a best segment time from a string and sets it for the active segment
        with the chosen timing method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_active_parse_and_set_best_segment_time(self.ptr, time.encode())
        return result

    def active_parse_and_set_comparison_time(self, comparison, time):
        """Parses a comparison time for the provided comparison and sets it for the
        active active segment with the chosen timing method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_active_parse_and_set_comparison_time(self.ptr, comparison.encode(), time.encode())
        return result

    def add_comparison(self, comparison):
        """Adds a new custom comparison. It can't be added if it starts with
        `[Race]` or already exists.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_add_comparison(self.ptr, comparison.encode())
        return result

    def import_comparison(self, run, comparison):
        """Imports the Personal Best from the provided run as a comparison. The
        comparison can't be added if its name starts with `[Race]` or it already
        exists.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if run.ptr == None:
            raise Exception("run is disposed")
        result = livesplit_core_native.RunEditor_import_comparison(self.ptr, run.ptr, comparison.encode())
        return result

    def remove_comparison(self, comparison):
        """Removes the chosen custom comparison. You can't remove a Comparison
        Generator's Comparison or the Personal Best.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_remove_comparison(self.ptr, comparison.encode())

    def rename_comparison(self, old_name, new_name):
        """Renames a comparison. The comparison can't be renamed if the new name of
        the comparison starts with `[Race]` or it already exists.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_rename_comparison(self.ptr, old_name.encode(), new_name.encode())
        return result

    def move_comparison(self, src_index, dst_index):
        """Reorders the custom comparisons by moving the comparison with the source
        index specified to the destination index specified. Returns False if one
        of the indices is invalid. The indices are based on the comparison names of
        the Run Editor's state.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_move_comparison(self.ptr, src_index, dst_index)
        return result

    def parse_and_generate_goal_comparison(self, time):
        """Parses a goal time and generates a custom goal comparison based on the
        parsed value. The comparison's times are automatically balanced based on the
        runner's history such that it roughly represents what split times for the
        goal time would roughly look like. Since it is populated by the runner's
        history, only goal times within the sum of the best segments and the sum of
        the worst segments are supported. Everything else is automatically capped by
        that range. The comparison is only populated for the selected timing method.
        The other timing method's comparison times are not modified by this, so you
        can call this again with the other timing method to generate the comparison
        times for both timing methods.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunEditor_parse_and_generate_goal_comparison(self.ptr, time.encode())
        return result

    def clear_history(self):
        """Clears out the Attempt History and the Segment Histories of all the
        segments.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_clear_history(self.ptr)

    def clear_times(self):
        """Clears out the Attempt History, the Segment Histories, all the times,
        sets the Attempt Count to 0 and clears the speedrun.com run id
        association. All Custom Comparisons other than `Personal Best` are
        deleted as well.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.RunEditor_clear_times(self.ptr)

    def clean_sum_of_best(self):
        """Creates a Sum of Best Cleaner which allows you to interactively remove
        potential issues in the segment history that lead to an inaccurate Sum
        of Best. If you skip a split, whenever you will do the next split, the
        combined segment time might be faster than the sum of the individual
        best segments. The Sum of Best Cleaner will point out all of these and
        allows you to delete them individually if any of them seem wrong.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SumOfBestCleaner(livesplit_core_native.RunEditor_clean_sum_of_best(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunEditor(RunEditorRefMut):
    """The Run Editor allows modifying Runs while ensuring that all the different
    invariants of the Run objects are upheld no matter what kind of operations
    are being applied to the Run. It provides the current state of the editor as
    state objects that can be visualized by any kind of User Interface.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(run):
        """Creates a new Run Editor that modifies the Run provided. Creation of the Run
        Editor fails when a Run with no segments is provided. If a Run object with
        no segments is provided, the Run Editor creation fails and None is
        returned.
        """
        if run.ptr == None:
            raise Exception("run is disposed")
        result = RunEditor(livesplit_core_native.RunEditor_new(run.ptr))
        run.ptr = None
        if result.ptr == None:
            return None
        return result

    def close(self):
        """Closes the Run Editor and gives back access to the modified Run object. In
        case you want to implement a Cancel Button, just dispose the Run object you
        get here.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Run(livesplit_core_native.RunEditor_close(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataRef:
    """The Run Metadata stores additional information about a run, like the
    platform and region of the game. All of this information is optional.
    """

    def run_id(self):
        """Accesses the speedrun.com Run ID of the run. This Run ID specify which
        Record on speedrun.com this run is associated with. This should be
        changed once the Personal Best doesn't match up with that record
        anymore. This may be empty if there's no association.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadata_run_id(self.ptr).decode()
        return result

    def platform_name(self):
        """Accesses the name of the platform this game is run on. This may be empty
        if it's not specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadata_platform_name(self.ptr).decode()
        return result

    def uses_emulator(self):
        """Returns True if this speedrun is done on an emulator. However False
        may also indicate that this information is simply not known.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadata_uses_emulator(self.ptr)
        return result

    def region_name(self):
        """Accesses the name of the region this game is from. This may be empty if
        it's not specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadata_region_name(self.ptr).decode()
        return result

    def speedrun_com_variables(self):
        """Returns an iterator iterating over all the speedrun.com variables and their
        values that have been specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunMetadataSpeedrunComVariablesIter(livesplit_core_native.RunMetadata_speedrun_com_variables(self.ptr))
        return result

    def custom_variables(self):
        """Returns an iterator iterating over all the custom variables and their
        values. This includes both temporary and permanent variables.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunMetadataCustomVariablesIter(livesplit_core_native.RunMetadata_custom_variables(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataRefMut(RunMetadataRef):
    """The Run Metadata stores additional information about a run, like the
    platform and region of the game. All of this information is optional.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadata(RunMetadataRefMut):
    """The Run Metadata stores additional information about a run, like the
    platform and region of the game. All of this information is optional.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariableRef:
    """A custom variable is a key value pair storing additional information about a
    run. Unlike the speedrun.com variables, these can be fully custom and don't
    need to correspond to anything on speedrun.com. Permanent custom variables
    can be specified by the runner. Additionally auto splitters or other sources
    may provide temporary custom variables that are not stored in the splits
    files.
    """

    def name(self):
        """Accesses the name of this custom variable.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadataCustomVariable_name(self.ptr).decode()
        return result

    def value(self):
        """Accesses the value of this custom variable.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadataCustomVariable_value(self.ptr).decode()
        return result

    def is_permanent(self):
        """Returns True if the custom variable is permanent. Permanent variables get
        stored in the splits file and are visible in the run editor. Temporary
        variables are not.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadataCustomVariable_is_permanent(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariableRefMut(RunMetadataCustomVariableRef):
    """A custom variable is a key value pair storing additional information about a
    run. Unlike the speedrun.com variables, these can be fully custom and don't
    need to correspond to anything on speedrun.com. Permanent custom variables
    can be specified by the runner. Additionally auto splitters or other sources
    may provide temporary custom variables that are not stored in the splits
    files.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariable(RunMetadataCustomVariableRefMut):
    """A custom variable is a key value pair storing additional information about a
    run. Unlike the speedrun.com variables, these can be fully custom and don't
    need to correspond to anything on speedrun.com. Permanent custom variables
    can be specified by the runner. Additionally auto splitters or other sources
    may provide temporary custom variables that are not stored in the splits
    files.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.RunMetadataCustomVariable_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariablesIterRef:
    """An iterator iterating over all the custom variables and their values
    that have been specified.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariablesIterRefMut(RunMetadataCustomVariablesIterRef):
    """An iterator iterating over all the custom variables and their values
    that have been specified.
    """

    def next(self):
        """Accesses the next custom variable. Returns None if there are no more
        variables.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunMetadataCustomVariableRef(livesplit_core_native.RunMetadataCustomVariablesIter_next(self.ptr))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataCustomVariablesIter(RunMetadataCustomVariablesIterRefMut):
    """An iterator iterating over all the custom variables and their values
    that have been specified.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.RunMetadataCustomVariablesIter_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariableRef:
    """A speedrun.com variable is an arbitrary key value pair storing additional
    information about the category. An example of this may be whether Amiibos
    are used in the category.
    """

    def name(self):
        """Accesses the name of this speedrun.com variable.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadataSpeedrunComVariable_name(self.ptr).decode()
        return result

    def value(self):
        """Accesses the value of this speedrun.com variable.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.RunMetadataSpeedrunComVariable_value(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariableRefMut(RunMetadataSpeedrunComVariableRef):
    """A speedrun.com variable is an arbitrary key value pair storing additional
    information about the category. An example of this may be whether Amiibos
    are used in the category.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariable(RunMetadataSpeedrunComVariableRefMut):
    """A speedrun.com variable is an arbitrary key value pair storing additional
    information about the category. An example of this may be whether Amiibos
    are used in the category.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.RunMetadataSpeedrunComVariable_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariablesIterRef:
    """An iterator iterating over all the speedrun.com variables and their values
    that have been specified.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariablesIterRefMut(RunMetadataSpeedrunComVariablesIterRef):
    """An iterator iterating over all the speedrun.com variables and their values
    that have been specified.
    """

    def next(self):
        """Accesses the next speedrun.com variable. Returns None if there are no more
        variables.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunMetadataSpeedrunComVariableRef(livesplit_core_native.RunMetadataSpeedrunComVariablesIter_next(self.ptr))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class RunMetadataSpeedrunComVariablesIter(RunMetadataSpeedrunComVariablesIterRefMut):
    """An iterator iterating over all the speedrun.com variables and their values
    that have been specified.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.RunMetadataSpeedrunComVariablesIter_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentRef:
    """A Segment describes a point in a speedrun that is suitable for storing a
    split time. This stores the name of that segment, an icon, the split times
    of different comparisons, and a history of segment times.
    """

    def name(self):
        """Accesses the name of the segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Segment_name(self.ptr).decode()
        return result

    def icon_ptr(self):
        """Accesses the segment icon's data. If there is no segment icon, this returns
        an empty buffer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Segment_icon_ptr(self.ptr)
        return result

    def icon_len(self):
        """Accesses the amount of bytes the segment icon's data takes up.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Segment_icon_len(self.ptr)
        return result

    def comparison(self, comparison):
        """Accesses the specified comparison's time. If there's none for this
        comparison, an empty time is being returned (but not stored in the
        segment).
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.Segment_comparison(self.ptr, comparison.encode()))
        return result

    def personal_best_split_time(self):
        """Accesses the split time of the Personal Best for this segment. If it
        doesn't exist, an empty time is returned.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.Segment_personal_best_split_time(self.ptr))
        return result

    def best_segment_time(self):
        """Accesses the Best Segment Time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.Segment_best_segment_time(self.ptr))
        return result

    def segment_history(self):
        """Accesses the Segment History of this segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SegmentHistoryRef(livesplit_core_native.Segment_segment_history(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentRefMut(SegmentRef):
    """A Segment describes a point in a speedrun that is suitable for storing a
    split time. This stores the name of that segment, an icon, the split times
    of different comparisons, and a history of segment times.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class Segment(SegmentRefMut):
    """A Segment describes a point in a speedrun that is suitable for storing a
    split time. This stores the name of that segment, an icon, the split times
    of different comparisons, and a history of segment times.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Segment_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(name):
        """Creates a new Segment with the name given.
        """
        result = Segment(livesplit_core_native.Segment_new(name.encode()))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryRef:
    """Stores the segment times achieved for a certain segment. Each segment is
    tagged with an index. Only segment times with an index larger than 0 are
    considered times actually achieved by the runner, while the others are
    artifacts of route changes and similar algorithmic changes.
    """

    def iter(self):
        """Iterates over all the segment times and their indices.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SegmentHistoryIter(livesplit_core_native.SegmentHistory_iter(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryRefMut(SegmentHistoryRef):
    """Stores the segment times achieved for a certain segment. Each segment is
    tagged with an index. Only segment times with an index larger than 0 are
    considered times actually achieved by the runner, while the others are
    artifacts of route changes and similar algorithmic changes.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistory(SegmentHistoryRefMut):
    """Stores the segment times achieved for a certain segment. Each segment is
    tagged with an index. Only segment times with an index larger than 0 are
    considered times actually achieved by the runner, while the others are
    artifacts of route changes and similar algorithmic changes.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryElementRef:
    """A segment time achieved for a segment. It is tagged with an index. Only
    segment times with an index larger than 0 are considered times actually
    achieved by the runner, while the others are artifacts of route changes and
    similar algorithmic changes.
    """

    def index(self):
        """Accesses the index of the segment history element.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SegmentHistoryElement_index(self.ptr)
        return result

    def time(self):
        """Accesses the segment time of the segment history element.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.SegmentHistoryElement_time(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryElementRefMut(SegmentHistoryElementRef):
    """A segment time achieved for a segment. It is tagged with an index. Only
    segment times with an index larger than 0 are considered times actually
    achieved by the runner, while the others are artifacts of route changes and
    similar algorithmic changes.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryElement(SegmentHistoryElementRefMut):
    """A segment time achieved for a segment. It is tagged with an index. Only
    segment times with an index larger than 0 are considered times actually
    achieved by the runner, while the others are artifacts of route changes and
    similar algorithmic changes.
    """

    def drop(self):
        if self.ptr != None:
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryIterRef:
    """Iterates over all the segment times of a segment and their indices.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryIterRefMut(SegmentHistoryIterRef):
    """Iterates over all the segment times of a segment and their indices.
    """

    def next(self):
        """Accesses the next Segment History element. Returns None if there are no
        more elements.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SegmentHistoryElementRef(livesplit_core_native.SegmentHistoryIter_next(self.ptr))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentHistoryIter(SegmentHistoryIterRefMut):
    """Iterates over all the segment times of a segment and their indices.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SegmentHistoryIter_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentTimeComponentRef:
    """The Segment Time Component is a component that shows the time for the current
    segment in a comparison of your choosing. If no comparison is specified it
    uses the timer's current comparison.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.SegmentTimeComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.SegmentTimeComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentTimeComponentRefMut(SegmentTimeComponentRef):
    """The Segment Time Component is a component that shows the time for the current
    segment in a comparison of your choosing. If no comparison is specified it
    uses the timer's current comparison.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SegmentTimeComponent(SegmentTimeComponentRefMut):
    """The Segment Time Component is a component that shows the time for the current
    segment in a comparison of your choosing. If no comparison is specified it
    uses the timer's current comparison.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SegmentTimeComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Segment Time Component.
        """
        result = SegmentTimeComponent(livesplit_core_native.SegmentTimeComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.SegmentTimeComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponentRef:
    """The Separator Component is a simple component that only serves to render
    separators between components.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponentRefMut(SeparatorComponentRef):
    """The Separator Component is a simple component that only serves to render
    separators between components.
    """

    def state(self):
        """Calculates the component's state.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SeparatorComponentState(livesplit_core_native.SeparatorComponent_state(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponent(SeparatorComponentRefMut):
    """The Separator Component is a simple component that only serves to render
    separators between components.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SeparatorComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Separator Component.
        """
        result = SeparatorComponent(livesplit_core_native.SeparatorComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.SeparatorComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponentStateRefMut(SeparatorComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SeparatorComponentState(SeparatorComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SeparatorComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SettingValueRef:
    """Describes a setting's value. Such a value can be of a variety of different
    types.
    """

    def as_json(self):
        """Encodes this Setting Value's state as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SettingValue_as_json(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SettingValueRefMut(SettingValueRef):
    """Describes a setting's value. Such a value can be of a variety of different
    types.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SettingValue(SettingValueRefMut):
    """Describes a setting's value. Such a value can be of a variety of different
    types.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SettingValue_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def from_bool(value):
        """Creates a new setting value from a boolean value.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_bool(value))
        return result

    @staticmethod
    def from_uint(value):
        """Creates a new setting value from an unsigned integer.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_uint(value))
        return result

    @staticmethod
    def from_int(value):
        """Creates a new setting value from a signed integer.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_int(value))
        return result

    @staticmethod
    def from_string(value):
        """Creates a new setting value from a string.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_string(value.encode()))
        return result

    @staticmethod
    def from_optional_string(value):
        """Creates a new setting value from a string that has the type `optional string`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_string(value.encode()))
        return result

    @staticmethod
    def from_optional_empty_string():
        """Creates a new empty setting value that has the type `optional string`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_empty_string())
        return result

    @staticmethod
    def from_accuracy(value):
        """Creates a new setting value from an accuracy name. If it doesn't match a
        known accuracy, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_accuracy(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_digits_format(value):
        """Creates a new setting value from a digits format name. If it doesn't match a
        known digits format, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_digits_format(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_optional_timing_method(value):
        """Creates a new setting value from a timing method name with the type
        `optional timing method`. If it doesn't match a known timing method, None
        is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_timing_method(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_optional_empty_timing_method():
        """Creates a new empty setting value with the type `optional timing method`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_empty_timing_method())
        return result

    @staticmethod
    def from_color(r, g, b, a):
        """Creates a new setting value from the color provided as RGBA.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_color(r, g, b, a))
        return result

    @staticmethod
    def from_optional_color(r, g, b, a):
        """Creates a new setting value from the color provided as RGBA with the type
        `optional color`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_color(r, g, b, a))
        return result

    @staticmethod
    def from_optional_empty_color():
        """Creates a new empty setting value with the type `optional color`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_optional_empty_color())
        return result

    @staticmethod
    def from_transparent_gradient():
        """Creates a new setting value that is a transparent gradient.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_transparent_gradient())
        return result

    @staticmethod
    def from_vertical_gradient(r1, g1, b1, a1, r2, g2, b2, a2):
        """Creates a new setting value from the vertical gradient provided as two RGBA colors.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_vertical_gradient(r1, g1, b1, a1, r2, g2, b2, a2))
        return result

    @staticmethod
    def from_horizontal_gradient(r1, g1, b1, a1, r2, g2, b2, a2):
        """Creates a new setting value from the horizontal gradient provided as two RGBA colors.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_horizontal_gradient(r1, g1, b1, a1, r2, g2, b2, a2))
        return result

    @staticmethod
    def from_alternating_gradient(r1, g1, b1, a1, r2, g2, b2, a2):
        """Creates a new setting value from the alternating gradient provided as two RGBA colors.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_alternating_gradient(r1, g1, b1, a1, r2, g2, b2, a2))
        return result

    @staticmethod
    def from_alignment(value):
        """Creates a new setting value from the alignment name provided. If it doesn't
        match a known alignment, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_alignment(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_column_kind(value):
        """Creates a new setting value from the column kind with the name provided. If
        it doesn't match a known column kind, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_column_kind(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_column_start_with(value):
        """Creates a new setting value from the column start with the name provided. If
        it doesn't match a known column start with, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_column_start_with(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_column_update_with(value):
        """Creates a new setting value from the column update with the name provided.
        If it doesn't match a known column update with, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_column_update_with(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_column_update_trigger(value):
        """Creates a new setting value from the column update trigger. If it doesn't
        match a known column update trigger, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_column_update_trigger(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_layout_direction(value):
        """Creates a new setting value from the layout direction. If it doesn't
        match a known layout direction, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_layout_direction(value.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_font(family, style, weight, stretch):
        """Creates a new setting value with the type `font`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_font(family.encode(), style.encode(), weight.encode(), stretch.encode()))
        if result.ptr == None:
            return None
        return result

    @staticmethod
    def from_empty_font():
        """Creates a new empty setting value with the type `font`.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_empty_font())
        return result

    @staticmethod
    def from_delta_gradient(value):
        """Creates a new setting value from the delta gradient with the name provided.
        If it doesn't match a known delta gradient, None is returned.
        """
        result = SettingValue(livesplit_core_native.SettingValue_from_delta_gradient(value.encode()))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SharedTimerRef:
    """A Shared Timer that can be used to share a single timer object with multiple
    owners.
    """

    def share(self):
        """Creates a new shared timer handle that shares the same timer. The inner
        timer object only gets disposed when the final handle gets disposed.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SharedTimer(livesplit_core_native.SharedTimer_share(self.ptr))
        return result

    def read(self):
        """Requests read access to the timer that is being shared. This blocks the
        thread as long as there is an active write lock. Dispose the read lock when
        you are done using the timer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimerReadLock(livesplit_core_native.SharedTimer_read(self.ptr))
        return result

    def write(self):
        """Requests write access to the timer that is being shared. This blocks the
        thread as long as there are active write or read locks. Dispose the write
        lock when you are done using the timer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimerWriteLock(livesplit_core_native.SharedTimer_write(self.ptr))
        return result

    def replace_inner(self, timer):
        """Replaces the timer that is being shared by the timer provided. This blocks
        the thread as long as there are active write or read locks. Everyone who is
        sharing the old timer will share the provided timer after successful
        completion.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        livesplit_core_native.SharedTimer_replace_inner(self.ptr, timer.ptr)
        timer.ptr = None

    def __init__(self, ptr):
        self.ptr = ptr

class SharedTimerRefMut(SharedTimerRef):
    """A Shared Timer that can be used to share a single timer object with multiple
    owners.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SharedTimer(SharedTimerRefMut):
    """A Shared Timer that can be used to share a single timer object with multiple
    owners.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SharedTimer_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SoftwareRendererRef:
    """The software renderer allows rendering layouts entirely on the CPU. This is
    surprisingly fast and can be considered the default renderer.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SoftwareRendererRefMut(SoftwareRendererRef):
    """The software renderer allows rendering layouts entirely on the CPU. This is
    surprisingly fast and can be considered the default renderer.
    """

    def render(self, layout_state, data, width, height, stride, force_redraw):
        """Renders the layout state provided into the image buffer provided. The image
        has to be an array of RGBA8 encoded pixels (red, green, blue, alpha with
        each channel being an u8). Some frameworks may over allocate an image's
        dimensions. So an image with dimensions 100x50 may be over allocated as
        128x64. In that case you provide the real dimensions of 100x50 as the width
        and height, but a stride of 128 pixels as that correlates with the real
        width of the underlying buffer. By default the renderer will try not to
        redraw parts of the image that haven't changed. You can force a redraw in
        case the image provided or its contents have changed.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if layout_state.ptr == None:
            raise Exception("layout_state is disposed")
        livesplit_core_native.SoftwareRenderer_render(self.ptr, layout_state.ptr, data, width, height, stride, force_redraw)

    def __init__(self, ptr):
        self.ptr = ptr

class SoftwareRenderer(SoftwareRendererRefMut):
    """The software renderer allows rendering layouts entirely on the CPU. This is
    surprisingly fast and can be considered the default renderer.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SoftwareRenderer_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new software renderer.
        """
        result = SoftwareRenderer(livesplit_core_native.SoftwareRenderer_new())
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponentRef:
    """The Splits Component is the main component for visualizing all the split
    times. Each segment is shown in a tabular fashion showing the segment icon,
    segment name, the delta compared to the chosen comparison, and the split
    time. The list provides scrolling functionality, so not every segment needs
    to be shown all the time.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponentRefMut(SplitsComponentRef):
    """The Splits Component is the main component for visualizing all the split
    times. Each segment is shown in a tabular fashion showing the segment icon,
    segment name, the delta compared to the chosen comparison, and the split
    time. The list provides scrolling functionality, so not every segment needs
    to be shown all the time.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.SplitsComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and layout settings
        provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = SplitsComponentState(livesplit_core_native.SplitsComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def scroll_up(self):
        """Scrolls up the window of the segments that are shown. Doesn't move the
        scroll window if it reaches the top of the segments.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_scroll_up(self.ptr)

    def scroll_down(self):
        """Scrolls down the window of the segments that are shown. Doesn't move the
        scroll window if it reaches the bottom of the segments.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_scroll_down(self.ptr)

    def set_visual_split_count(self, count):
        """The amount of segments to show in the list at any given time. If this is
        set to 0, all the segments are shown. If this is set to a number lower
        than the total amount of segments, only a certain window of all the
        segments is shown. This window can scroll up or down.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_set_visual_split_count(self.ptr, count)

    def set_split_preview_count(self, count):
        """If there's more segments than segments that are shown, the window
        showing the segments automatically scrolls up and down when the current
        segment changes. This count determines the minimum number of future
        segments to be shown in this scrolling window when it automatically
        scrolls.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_set_split_preview_count(self.ptr, count)

    def set_always_show_last_split(self, always_show_last_split):
        """If not every segment is shown in the scrolling window of segments, then
        this determines whether the final segment is always to be shown, as it
        contains valuable information about the total duration of the chosen
        comparison, which is often the runner's Personal Best.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_set_always_show_last_split(self.ptr, always_show_last_split)

    def set_separator_last_split(self, separator_last_split):
        """If the last segment is to always be shown, this determines whether to
        show a more pronounced separator in front of the last segment, if it is
        not directly adjacent to the segment shown right before it in the
        scrolling window.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.SplitsComponent_set_separator_last_split(self.ptr, separator_last_split)

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponent(SplitsComponentRefMut):
    """The Splits Component is the main component for visualizing all the split
    times. Each segment is shown in a tabular fashion showing the segment icon,
    segment name, the delta compared to the chosen comparison, and the split
    time. The list provides scrolling functionality, so not every segment needs
    to be shown all the time.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SplitsComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Splits Component.
        """
        result = SplitsComponent(livesplit_core_native.SplitsComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.SplitsComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponentStateRef:
    """The state object that describes a single segment's information to visualize.
    """

    def final_separator_shown(self):
        """Describes whether a more pronounced separator should be shown in front of
        the last segment provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_final_separator_shown(self.ptr)
        return result

    def len(self):
        """Returns the amount of segments to visualize.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_len(self.ptr)
        return result

    def icon_change_count(self):
        """Returns the amount of icon changes that happened in this state object.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_icon_change_count(self.ptr)
        return result

    def icon_change_segment_index(self, icon_change_index):
        """Accesses the index of the segment of the icon change with the specified
        index. This is based on the index in the run, not on the index of the
        SplitState in the State object. The corresponding index is the index field
        of the SplitState object. You may not provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_icon_change_segment_index(self.ptr, icon_change_index)
        return result

    def icon_change_icon_ptr(self, icon_change_index):
        """The icon data of the segment of the icon change with the specified index.
        The buffer may be empty. This indicates that there is no icon. You may not
        provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_icon_change_icon_ptr(self.ptr, icon_change_index)
        return result

    def icon_change_icon_len(self, icon_change_index):
        """The length of the icon data of the segment of the icon change with the
        specified index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_icon_change_icon_len(self.ptr, icon_change_index)
        return result

    def name(self, index):
        """The name of the segment with the specified index. You may not provide an out
        of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_name(self.ptr, index).decode()
        return result

    def columns_len(self, index):
        """The amount of columns to visualize for the segment with the specified index.
        The columns are specified from right to left. You may not provide an out of
        bounds index. The amount of columns to visualize may differ from segment to
        segment.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_columns_len(self.ptr, index)
        return result

    def column_value(self, index, column_index):
        """The column's value to show for the split and column with the specified
        index. The columns are specified from right to left. You may not provide an
        out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_column_value(self.ptr, index, column_index).decode()
        return result

    def column_semantic_color(self, index, column_index):
        """The semantic coloring information the column's value carries of the segment
        and column with the specified index. The columns are specified from right to
        left. You may not provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_column_semantic_color(self.ptr, index, column_index).decode()
        return result

    def is_current_split(self, index):
        """Describes if the segment with the specified index is the segment the active
        attempt is currently on.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_is_current_split(self.ptr, index)
        return result

    def has_column_labels(self):
        """Describes if the columns have labels that are meant to be shown. If this is
        `false`, no labels are supposed to be visualized.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_has_column_labels(self.ptr)
        return result

    def column_label(self, index):
        """Returns the label of the column specified. The list is specified from right
        to left. You may not provide an out of bounds index.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.SplitsComponentState_column_label(self.ptr, index).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponentStateRefMut(SplitsComponentStateRef):
    """The state object that describes a single segment's information to visualize.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SplitsComponentState(SplitsComponentStateRefMut):
    """The state object that describes a single segment's information to visualize.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SplitsComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestCleanerRef:
    """A Sum of Best Cleaner allows you to interactively remove potential issues in
    the Segment History that lead to an inaccurate Sum of Best. If you skip a
    split, whenever you get to the next split, the combined segment time might
    be faster than the sum of the individual best segments. The Sum of Best
    Cleaner will point out all of occurrences of this and allows you to delete
    them individually if any of them seem wrong.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestCleanerRefMut(SumOfBestCleanerRef):
    """A Sum of Best Cleaner allows you to interactively remove potential issues in
    the Segment History that lead to an inaccurate Sum of Best. If you skip a
    split, whenever you get to the next split, the combined segment time might
    be faster than the sum of the individual best segments. The Sum of Best
    Cleaner will point out all of occurrences of this and allows you to delete
    them individually if any of them seem wrong.
    """

    def next_potential_clean_up(self):
        """Returns the next potential clean up. If there are no more potential
        clean ups, None is returned.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = PotentialCleanUp(livesplit_core_native.SumOfBestCleaner_next_potential_clean_up(self.ptr))
        if result.ptr == None:
            return None
        return result

    def apply(self, clean_up):
        """Applies a clean up to the Run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if clean_up.ptr == None:
            raise Exception("clean_up is disposed")
        livesplit_core_native.SumOfBestCleaner_apply(self.ptr, clean_up.ptr)
        clean_up.ptr = None

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestCleaner(SumOfBestCleanerRefMut):
    """A Sum of Best Cleaner allows you to interactively remove potential issues in
    the Segment History that lead to an inaccurate Sum of Best. If you skip a
    split, whenever you get to the next split, the combined segment time might
    be faster than the sum of the individual best segments. The Sum of Best
    Cleaner will point out all of occurrences of this and allows you to delete
    them individually if any of them seem wrong.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SumOfBestCleaner_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestComponentRef:
    """The Sum of Best Segments Component shows the fastest possible time to
    complete a run of this category, based on information collected from all the
    previous attempts. This often matches up with the sum of the best segment
    times of all the segments, but that may not always be the case, as skipped
    segments may introduce combined segments that may be faster than the actual
    sum of their best segment times. The name is therefore a bit misleading, but
    sticks around for historical reasons.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.SumOfBestComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.SumOfBestComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestComponentRefMut(SumOfBestComponentRef):
    """The Sum of Best Segments Component shows the fastest possible time to
    complete a run of this category, based on information collected from all the
    previous attempts. This often matches up with the sum of the best segment
    times of all the segments, but that may not always be the case, as skipped
    segments may introduce combined segments that may be faster than the actual
    sum of their best segment times. The name is therefore a bit misleading, but
    sticks around for historical reasons.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class SumOfBestComponent(SumOfBestComponentRefMut):
    """The Sum of Best Segments Component shows the fastest possible time to
    complete a run of this category, based on information collected from all the
    previous attempts. This often matches up with the sum of the best segment
    times of all the segments, but that may not always be the case, as skipped
    segments may introduce combined segments that may be faster than the actual
    sum of their best segment times. The name is therefore a bit misleading, but
    sticks around for historical reasons.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.SumOfBestComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Sum of Best Segments Component.
        """
        result = SumOfBestComponent(livesplit_core_native.SumOfBestComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.SumOfBestComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponentRef:
    """The Text Component simply visualizes any given text. This can either be a
    single centered text, or split up into a left and right text, which is
    suitable for a situation where you have a label and a value.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.TextComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = TextComponentState(livesplit_core_native.TextComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponentRefMut(TextComponentRef):
    """The Text Component simply visualizes any given text. This can either be a
    single centered text, or split up into a left and right text, which is
    suitable for a situation where you have a label and a value.
    """

    def set_center(self, text):
        """Sets the centered text. If the current mode is split, it is switched to
        centered mode.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.TextComponent_set_center(self.ptr, text.encode())

    def set_left(self, text):
        """Sets the left text. If the current mode is centered, it is switched to
        split mode, with the right text being empty.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.TextComponent_set_left(self.ptr, text.encode())

    def set_right(self, text):
        """Sets the right text. If the current mode is centered, it is switched to
        split mode, with the left text being empty.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.TextComponent_set_right(self.ptr, text.encode())

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponent(TextComponentRefMut):
    """The Text Component simply visualizes any given text. This can either be a
    single centered text, or split up into a left and right text, which is
    suitable for a situation where you have a label and a value.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TextComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Text Component.
        """
        result = TextComponent(livesplit_core_native.TextComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.TextComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def left(self):
        """Accesses the left part of the text. If the text isn't split up, an empty
        string is returned instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TextComponentState_left(self.ptr).decode()
        return result

    def right(self):
        """Accesses the right part of the text. If the text isn't split up, an empty
        string is returned instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TextComponentState_right(self.ptr).decode()
        return result

    def center(self):
        """Accesses the centered text. If the text isn't centered, an empty string is
        returned instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TextComponentState_center(self.ptr).decode()
        return result

    def is_split(self):
        """Returns whether the text is split up into a left and right part.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TextComponentState_is_split(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponentStateRefMut(TextComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TextComponentState(TextComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TextComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TimeRef:
    """A time that can store a Real Time and a Game Time. Both of them are
    optional.
    """

    def clone(self):
        """Clones the time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Time(livesplit_core_native.Time_clone(self.ptr))
        return result

    def real_time(self):
        """The Real Time value. This may be None if this time has no Real Time value.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Time_real_time(self.ptr))
        if result.ptr == None:
            return None
        return result

    def game_time(self):
        """The Game Time value. This may be None if this time has no Game Time value.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Time_game_time(self.ptr))
        if result.ptr == None:
            return None
        return result

    def index(self, timing_method):
        """Access the time's value for the timing method specified.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Time_index(self.ptr, timing_method))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimeRefMut(TimeRef):
    """A time that can store a Real Time and a Game Time. Both of them are
    optional.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class Time(TimeRefMut):
    """A time that can store a Real Time and a Game Time. Both of them are
    optional.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Time_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TimeSpanRef:
    """A Time Span represents a certain span of time.
    """

    def clone(self):
        """Clones the Time Span.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpan(livesplit_core_native.TimeSpan_clone(self.ptr))
        return result

    def total_seconds(self) -> float:
        """Returns the total amount of seconds (including decimals) this Time Span
        represents.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TimeSpan_total_seconds(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimeSpanRefMut(TimeSpanRef):
    """A Time Span represents a certain span of time.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TimeSpan(TimeSpanRefMut):
    """A Time Span represents a certain span of time.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TimeSpan_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def from_seconds(seconds):
        """Creates a new Time Span from a given amount of seconds.
        """
        result = TimeSpan(livesplit_core_native.TimeSpan_from_seconds(seconds))
        return result

    @staticmethod
    def parse(text):
        """Parses a Time Span from a string. Returns None if the time can't be
        parsed.
        """
        result = TimeSpan(livesplit_core_native.TimeSpan_parse(text.encode()))
        if result.ptr == None:
            return None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerRef:
    """A Timer provides all the capabilities necessary for doing speedrun attempts.
    """

    def current_split_index(self):
        """Accesses the index of the split the attempt is currently on. If there's
        no attempt in progress, `-1` is returned instead. This returns an
        index that is equal to the amount of segments when the attempt is
        finished, but has not been reset. So you need to be careful when using
        this value for indexing.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_current_split_index(self.ptr)
        return result

    def current_timing_method(self):
        """Returns the currently selected Timing Method.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_current_timing_method(self.ptr)
        return result

    def current_comparison(self):
        """Returns the current comparison that is being compared against. This may
        be a custom comparison or one of the Comparison Generators.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_current_comparison(self.ptr).decode()
        return result

    def is_game_time_initialized(self):
        """Returns whether Game Time is currently initialized. Game Time
        automatically gets uninitialized for each new attempt.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_is_game_time_initialized(self.ptr)
        return result

    def is_game_time_paused(self):
        """Returns whether the Game Timer is currently paused. If the Game Timer is
        not paused, it automatically increments similar to Real Time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_is_game_time_paused(self.ptr)
        return result

    def loading_times(self):
        """Accesses the loading times. Loading times are defined as Game Time - Real Time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeSpanRef(livesplit_core_native.Timer_loading_times(self.ptr))
        return result

    def current_phase(self):
        """Returns the current Timer Phase.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_current_phase(self.ptr)
        return result

    def get_run(self):
        """Accesses the Run in use by the Timer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = RunRef(livesplit_core_native.Timer_get_run(self.ptr))
        return result

    def save_as_lss(self):
        """Saves the Run in use by the Timer as a LiveSplit splits file (*.lss).
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.Timer_save_as_lss(self.ptr).decode()
        return result

    def print_debug(self):
        """Prints out debug information representing the whole state of the Timer. This
        is being written to stdout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_print_debug(self.ptr)

    def current_time(self):
        """Returns the current time of the Timer. The Game Time is None if the Game
        Time has not been initialized.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimeRef(livesplit_core_native.Timer_current_time(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerRefMut(TimerRef):
    """A Timer provides all the capabilities necessary for doing speedrun attempts.
    """

    def replace_run(self, run, update_splits):
        """Replaces the Run object used by the Timer with the Run object provided. If
        the Run provided contains no segments, it can't be used for timing and is
        not being modified. Otherwise the Run that was in use by the Timer gets
        stored in the Run object provided. Before the Run is returned, the current
        attempt is reset and the splits are being updated depending on the
        `update_splits` parameter. The return value indicates whether the Run got
        replaced successfully.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if run.ptr == None:
            raise Exception("run is disposed")
        result = livesplit_core_native.Timer_replace_run(self.ptr, run.ptr, update_splits)
        return result

    def set_run(self, run):
        """Sets the Run object used by the Timer with the Run object provided. If the
        Run provided contains no segments, it can't be used for timing and gets
        returned again. If the Run object can be set, the original Run object in use
        by the Timer is disposed by this method and None is returned.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if run.ptr == None:
            raise Exception("run is disposed")
        result = Run(livesplit_core_native.Timer_set_run(self.ptr, run.ptr))
        run.ptr = None
        if result.ptr == None:
            return None
        return result

    def start(self):
        """Starts the Timer if there is no attempt in progress. If that's not the
        case, nothing happens.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_start(self.ptr)

    def split(self):
        """If an attempt is in progress, stores the current time as the time of the
        current split. The attempt ends if the last split time is stored.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_split(self.ptr)

    def split_or_start(self):
        """Starts a new attempt or stores the current time as the time of the
        current split. The attempt ends if the last split time is stored.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_split_or_start(self.ptr)

    def skip_split(self):
        """Skips the current split if an attempt is in progress and the
        current split is not the last split.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_skip_split(self.ptr)

    def undo_split(self):
        """Removes the split time from the last split if an attempt is in progress
        and there is a previous split. The Timer Phase also switches to
        `Running` if it previously was `Ended`.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_undo_split(self.ptr)

    def reset(self, update_splits):
        """Resets the current attempt if there is one in progress. If the splits
        are to be updated, all the information of the current attempt is stored
        in the Run's history. Otherwise the current attempt's information is
        discarded.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_reset(self.ptr, update_splits)

    def reset_and_set_attempt_as_pb(self):
        """Resets the current attempt if there is one in progress. The splits are
        updated such that the current attempt's split times are being stored as
        the new Personal Best.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_reset_and_set_attempt_as_pb(self.ptr)

    def pause(self):
        """Pauses an active attempt that is not paused.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_pause(self.ptr)

    def resume(self):
        """Resumes an attempt that is paused.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_resume(self.ptr)

    def toggle_pause(self):
        """Toggles an active attempt between `Paused` and `Running`.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_toggle_pause(self.ptr)

    def toggle_pause_or_start(self):
        """Toggles an active attempt between `Paused` and `Running` or starts an
        attempt if there's none in progress.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_toggle_pause_or_start(self.ptr)

    def undo_all_pauses(self):
        """Removes all the pause times from the current time. If the current
        attempt is paused, it also resumes that attempt. Additionally, if the
        attempt is finished, the final split time is adjusted to not include the
        pause times as well.
        
        # Warning
        
        This behavior is not entirely optimal, as generally only the final split
        time is modified, while all other split times are left unmodified, which
        may not be what actually happened during the run.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_undo_all_pauses(self.ptr)

    def set_current_timing_method(self, method):
        """Sets the current Timing Method to the Timing Method provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_set_current_timing_method(self.ptr, method)

    def switch_to_next_comparison(self):
        """Switches the current comparison to the next comparison in the list.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_switch_to_next_comparison(self.ptr)

    def switch_to_previous_comparison(self):
        """Switches the current comparison to the previous comparison in the list.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_switch_to_previous_comparison(self.ptr)

    def initialize_game_time(self):
        """Initializes Game Time for the current attempt. Game Time automatically
        gets uninitialized for each new attempt.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_initialize_game_time(self.ptr)

    def deinitialize_game_time(self):
        """Deinitializes Game Time for the current attempt.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_deinitialize_game_time(self.ptr)

    def pause_game_time(self):
        """Pauses the Game Timer such that it doesn't automatically increment
        similar to Real Time.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_pause_game_time(self.ptr)

    def resume_game_time(self):
        """Resumes the Game Timer such that it automatically increments similar to
        Real Time, starting from the Game Time it was paused at.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_resume_game_time(self.ptr)

    def set_game_time(self, time):
        """Sets the Game Time to the time specified. This also works if the Game
        Time is paused, which can be used as a way of updating the Game Timer
        periodically without it automatically moving forward. This ensures that
        the Game Timer never shows any time that is not coming from the game.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if time.ptr == None:
            raise Exception("time is disposed")
        livesplit_core_native.Timer_set_game_time(self.ptr, time.ptr)

    def set_loading_times(self, time):
        """Instead of setting the Game Time directly, this method can be used to
        just specify the amount of time the game has been loading. The Game Time
        is then automatically determined by Real Time - Loading Times.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if time.ptr == None:
            raise Exception("time is disposed")
        livesplit_core_native.Timer_set_loading_times(self.ptr, time.ptr)

    def mark_as_unmodified(self):
        """Marks the Run as unmodified, so that it is known that all the changes
        have been saved.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        livesplit_core_native.Timer_mark_as_unmodified(self.ptr)

    def __init__(self, ptr):
        self.ptr = ptr

class Timer(TimerRefMut):
    """A Timer provides all the capabilities necessary for doing speedrun attempts.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.Timer_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new(run):
        """Creates a new Timer based on a Run object storing all the information
        about the splits. The Run object needs to have at least one segment, so
        that the Timer can store the final time. If a Run object with no
        segments is provided, the Timer creation fails and None is returned.
        """
        if run.ptr == None:
            raise Exception("run is disposed")
        result = Timer(livesplit_core_native.Timer_new(run.ptr))
        run.ptr = None
        if result.ptr == None:
            return None
        return result

    def into_shared(self):
        """Consumes the Timer and creates a Shared Timer that can be shared across
        multiple threads with multiple owners.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = SharedTimer(livesplit_core_native.Timer_into_shared(self.ptr))
        self.ptr = None
        return result

    def into_run(self, update_splits):
        """Takes out the Run from the Timer and resets the current attempt if there
        is one in progress. If the splits are to be updated, all the information
        of the current attempt is stored in the Run's history. Otherwise the
        current attempt's information is discarded.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Run(livesplit_core_native.Timer_into_run(self.ptr, update_splits))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponentRef:
    """The Timer Component is a component that shows the total time of the current
    attempt as a digital clock. The color of the time shown is based on a how
    well the current attempt is doing compared to the chosen comparison.
    """

    def state_as_json(self, timer, layout_settings):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = livesplit_core_native.TimerComponent_state_as_json(self.ptr, timer.ptr, layout_settings.ptr)
        return result

    def state(self, timer, layout_settings):
        """Calculates the component's state based on the timer and the layout
        settings provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        if layout_settings.ptr == None:
            raise Exception("layout_settings is disposed")
        result = TimerComponentState(livesplit_core_native.TimerComponent_state(self.ptr, timer.ptr, layout_settings.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponentRefMut(TimerComponentRef):
    """The Timer Component is a component that shows the total time of the current
    attempt as a digital clock. The color of the time shown is based on a how
    well the current attempt is doing compared to the chosen comparison.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponent(TimerComponentRefMut):
    """The Timer Component is a component that shows the total time of the current
    attempt as a digital clock. The color of the time shown is based on a how
    well the current attempt is doing compared to the chosen comparison.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TimerComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Timer Component.
        """
        result = TimerComponent(livesplit_core_native.TimerComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.TimerComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def time(self):
        """The time shown by the component without the fractional part.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TimerComponentState_time(self.ptr).decode()
        return result

    def fraction(self):
        """The fractional part of the time shown (including the dot).
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TimerComponentState_fraction(self.ptr).decode()
        return result

    def semantic_color(self):
        """The semantic coloring information the time carries.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TimerComponentState_semantic_color(self.ptr).decode()
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponentStateRefMut(TimerComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TimerComponentState(TimerComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TimerComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TimerReadLockRef:
    """A Timer Read Lock allows temporary read access to a timer. Dispose this to
    release the read lock.
    """

    def timer(self):
        """Accesses the timer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimerRef(livesplit_core_native.TimerReadLock_timer(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerReadLockRefMut(TimerReadLockRef):
    """A Timer Read Lock allows temporary read access to a timer. Dispose this to
    release the read lock.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TimerReadLock(TimerReadLockRefMut):
    """A Timer Read Lock allows temporary read access to a timer. Dispose this to
    release the read lock.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TimerReadLock_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TimerWriteLockRef:
    """A Timer Write Lock allows temporary write access to a timer. Dispose this to
    release the write lock.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TimerWriteLockRefMut(TimerWriteLockRef):
    """A Timer Write Lock allows temporary write access to a timer. Dispose this to
    release the write lock.
    """

    def timer(self):
        """Accesses the timer.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = TimerRefMut(livesplit_core_native.TimerWriteLock_timer(self.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TimerWriteLock(TimerWriteLockRefMut):
    """A Timer Write Lock allows temporary write access to a timer. Dispose this to
    release the write lock.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TimerWriteLock_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponentRef:
    """The Title Component is a component that shows the name of the game and the
    category that is being run. Additionally, the game icon, the attempt count,
    and the total number of successfully finished runs can be shown.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponentRefMut(TitleComponentRef):
    """The Title Component is a component that shows the name of the game and the
    category that is being run. Additionally, the game icon, the attempt count,
    and the total number of successfully finished runs can be shown.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.TitleComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = TitleComponentState(livesplit_core_native.TitleComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponent(TitleComponentRefMut):
    """The Title Component is a component that shows the name of the game and the
    category that is being run. Additionally, the game icon, the attempt count,
    and the total number of successfully finished runs can be shown.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TitleComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Title Component.
        """
        result = TitleComponent(livesplit_core_native.TitleComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.TitleComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponentStateRef:
    """The state object describes the information to visualize for this component.
    """

    def icon_change_ptr(self):
        """The data of the game's icon. This value is only specified whenever the icon
        changes. If you explicitly want to query this value, remount the component.
        The buffer may be empty. This indicates that there is no icon. If no change
        occurred, None is returned instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_icon_change_ptr(self.ptr)
        return result

    def icon_change_len(self):
        """The length of the game's icon data.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_icon_change_len(self.ptr)
        return result

    def line1(self):
        """The first title line to show. This is either the game's name, or a
        combination of the game's name and the category.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_line1(self.ptr).decode()
        return result

    def line2(self):
        """By default the category name is shown on the second line. Based on the
        settings, it can however instead be shown in a single line together with
        the game name. In that case None is returned instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_line2(self.ptr).decode()
        return result

    def is_centered(self):
        """Specifies whether the title should centered or aligned to the left
        instead.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_is_centered(self.ptr)
        return result

    def shows_finished_runs(self):
        """Returns whether the amount of successfully finished attempts is supposed to
        be shown.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_shows_finished_runs(self.ptr)
        return result

    def finished_runs(self):
        """Returns the amount of successfully finished attempts.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_finished_runs(self.ptr)
        return result

    def shows_attempts(self):
        """Returns whether the amount of total attempts is supposed to be shown.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_shows_attempts(self.ptr)
        return result

    def attempts(self):
        """Returns the amount of total attempts.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = livesplit_core_native.TitleComponentState_attempts(self.ptr)
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponentStateRefMut(TitleComponentStateRef):
    """The state object describes the information to visualize for this component.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TitleComponentState(TitleComponentStateRefMut):
    """The state object describes the information to visualize for this component.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TitleComponentState_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    def __init__(self, ptr):
        self.ptr = ptr

class TotalPlaytimeComponentRef:
    """The Total Playtime Component is a component that shows the total amount of
    time that the current category has been played for.
    """

    def __init__(self, ptr):
        self.ptr = ptr

class TotalPlaytimeComponentRefMut(TotalPlaytimeComponentRef):
    """The Total Playtime Component is a component that shows the total amount of
    time that the current category has been played for.
    """

    def state_as_json(self, timer):
        """Encodes the component's state information as JSON.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = livesplit_core_native.TotalPlaytimeComponent_state_as_json(self.ptr, timer.ptr)
        return result

    def state(self, timer):
        """Calculates the component's state based on the timer provided.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        if timer.ptr == None:
            raise Exception("timer is disposed")
        result = KeyValueComponentState(livesplit_core_native.TotalPlaytimeComponent_state(self.ptr, timer.ptr))
        return result

    def __init__(self, ptr):
        self.ptr = ptr

class TotalPlaytimeComponent(TotalPlaytimeComponentRefMut):
    """The Total Playtime Component is a component that shows the total amount of
    time that the current category has been played for.
    """

    def drop(self):
        if self.ptr != None:
            livesplit_core_native.TotalPlaytimeComponent_drop(self.ptr)
            self.ptr = None

    def __del__(self):
        self.drop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop()

    @staticmethod
    def new():
        """Creates a new Total Playtime Component.
        """
        result = TotalPlaytimeComponent(livesplit_core_native.TotalPlaytimeComponent_new())
        return result

    def into_generic(self):
        """Converts the component into a generic component suitable for using with a
        layout.
        """
        if self.ptr == None:
            raise Exception("self is disposed")
        result = Component(livesplit_core_native.TotalPlaytimeComponent_into_generic(self.ptr))
        self.ptr = None
        return result

    def __init__(self, ptr):
        self.ptr = ptr
