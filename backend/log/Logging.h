#ifndef LOGGING_H
#define LOGGING_H

#include<iostream>
//#include<ostream>

namespace naivecompiler
{

#define Logging( logType , message , ...) \
	do{ \
        if( Log::IsWritable( logType ) )\
        {\
            Log::BannerWrite( logType , __FUNCTION__ , message ,## __VA_ARGS__ ) ;\
        }\
	} while( 0 )


typedef int LogSeverity;

const int LOG_DEBUG=0, LOG_INFO = 1, LOG_WARNING = 2, LOG_ERROR = 3, LOG_FATAL = 4,
  NUM_SEVERITIES = 5;


class Log {
public:
    static inline Log& GetCurrentLog( void )
    {
        return currentLog ;
    }

    static inline void SetLevel( const LogSeverity logType )
    {
        GetCurrentLog().logLevel = CheckLogType( logType ) ;
    }

    static inline LogSeverity GetLevel( void )
    {
        return GetCurrentLog().logLevel ;
    }

    static void InitLogging(LogSeverity level) {
    	GetCurrentLog().SetLevel(level);
    }

    static void ShutdownLogging() {

    }
private:
    static inline LogSeverity CheckLogType( LogSeverity logType )
    {
        if( LOG_DEBUG > logType )
        {
            return LOG_DEBUG ;
        }

        if( LOG_FATAL < logType )
        {
            return LOG_FATAL ;
        }

        return logType ;
    }

    static Log currentLog;
    LogSeverity logLevel ;
};


// copy from glog



//#define LOG(severity) COMPACT_GOOGLE_LOG_ ## severity.stream()

#define LOGGING(severity) naivecompiler::LogMessage(__FUNCTION__, __LINE__, severity).stream()

#define LOG(severity) naivecompiler::LogMessage(severity).stream()

#if defined(DEBUG)
#define DLOG(severity) LOG(severity)
#else  // !DCHECK_IS_ON()
#define DLOG(severity) nullstream
#endif

class LogMessageVoidify {
 public:
  LogMessageVoidify() { }
  // This has to be an operator with a precedence lower than << but
  // higher than ?:
  void operator&(std::ostream&) { }
};

// https://stackoverflow.com/questions/11826554/standard-no-op-output-stream/11826787
//Use NullBuffer will overwrite stream_ class member for hole session, don't use it
class NullBuffer : public std::streambuf
{
public:
  int overflow(int c) { return c; }
};

class NullStream : public std::ostream { public: NullStream() : std::ostream(&m_sb) {} private: NullBuffer m_sb; };

static NullStream nullstream;

class LogMessage {

public:
	std::ostream& stream() {
		return *stream_;
	}

	LogMessage(LogSeverity severity) : funcname_(funcname_),
			severity_(severity), stream_(&std::cout) {
		if ( Log::GetLevel() > severity_) {
//			NullBuffer null_buffer;
//			stream_->rdbuf(&null_buffer);
			stream_= &nullstream;
		}
	}

	LogMessage(const char* funcname, int line, LogSeverity severity) : funcname_(funcname_),
			severity_(severity), stream_(&std::cout) {
		if ( Log::GetLevel() <= severity_) {
//		    std::streambuf * buf;
//		    buf = std::cout.rdbuf();
//		    stream_ = std::ostream(buf);
		} else {
			NullBuffer null_buffer;
			stream_->rdbuf(&null_buffer);
		}
		if ( Log::GetLevel() <= severity_) {
			stream() << funcname_ << ":" << line << "    " ;
		}
	}

	~LogMessage() {
	}
private:
	LogSeverity severity_;
	const char * funcname_;
	std::ostream* stream_;
};

}
#endif
