#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import threading




class demodulater(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.048e6
        self.quad_rate = quad_rate = samp_rate / 8
        self.audio_rate = audio_rate = quad_rate / 8

        ##################################################
        # Blocks
        ##################################################

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(8, firdes.low_pass(1.0, samp_rate, 70e3, 20e3, window.WIN_HAMMING), 700e3, samp_rate)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            '/home/abdyrazakov/Documents/Codex/2026-09-12/referenced-chatgpt-conversation-this-is-an/outputs/fm_test_omur.wav',
            1,
            int(audio_rate),
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, (2*samp_rate), True, 0 if "auto" == "auto" else max( int(float(0.1) * (2*samp_rate)) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff((1.0 / 128.0))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((1.0 / 128.0))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/abdyrazakov/Documents/Codex/2026-09-12/referenced-chatgpt-conversation-this-is-an/outputs/omur_zymyrayt_wbfm_192ksps.cf32', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_char*1, 1)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff((-1.0))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-1.0))
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quad_rate,
        	audio_decimation=8,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_wfm_rcv_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_quad_rate(self.samp_rate / 8)
        self.blocks_throttle2_0.set_sample_rate((2*self.samp_rate))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 70e3, 20e3, window.WIN_HAMMING))

    def get_quad_rate(self):
        return self.quad_rate

    def set_quad_rate(self, quad_rate):
        self.quad_rate = quad_rate
        self.set_audio_rate(self.quad_rate / 8)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate




def main(top_block_cls=demodulater, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    tb.wait()


if __name__ == '__main__':
    main()
