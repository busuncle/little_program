#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/event.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>


const static int port = 1234;
const static char* ip = "127.0.0.1";
const static int MAX_EVENT_COUNT = 5000;
const static int MAX_RECV_BUFF = 65535;

int listener;
char buf[MAX_RECV_BUFF];

int create_listener();
int register_fd(int kq, int fd);
void wait_event(int kq);
void handle_event(int kq, struct kevent* events, int nevents);
void accept_conn(int kq, int conn_size);
void receive(int sock, int avail_bytes);


int create_listener()
{
	int sock = socket(PF_INET, SOCK_STREAM, 0);
	if (sock == -1)
	{
		printf("create socket failed: %d\n", errno);
		return -1;
	}

	int optval = 1;
	setsockopt(sock, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval));

	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = inet_addr(ip);
	if (bind(sock, (struct sockaddr*)&addr, sizeof(struct sockaddr)) == -1)
	{
		printf("bind socket failed: %d\n", errno);
		return -1;
	}

	if (listen(sock, 5) == -1)
	{
		printf("listen socket failed: %d\n", errno);
		return -1;
	}

	return sock;
}


int register_fd(int kq, int fd)
{
	struct kevent changes[1];
	EV_SET(&changes[0], fd, EVFILT_READ, EV_ADD, 0, 0, NULL);

	int ret = kevent(kq, changes, 1, NULL, 0, NULL);
	if (ret == -1) return 0;
	return 1;
}


void wait_event(int kq)
{
	struct kevent events[MAX_EVENT_COUNT];
	while(1)
	{
		int ret = kevent(kq, NULL, 0, events, MAX_EVENT_COUNT, NULL);
		if (ret == -1)
		{
			printf("kevent failed!\n");
			continue;
		}
		handle_event(kq, events, ret);
	}
}


void handle_event(int kq, struct kevent* events, int nevents)
{
	for(int i = 0; i < nevents; i++)
	{
		int sock = events[i].ident;
		int data = events[i].data;
		if (sock == listener)
		{
			accept_conn(kq, data);
		}
		else
		{
			receive(sock, data);
		}
	}
}


void accept_conn(int kq, int conn_size)
{
	for(int i = 0; i < conn_size; i++)
	{
		int client = accept(listener, NULL, NULL);
		if (client == -1)
		{
			printf("accept failed \n");
			continue;
		}

		if (!register_fd(kq, client))
		{
			printf("register client failed \n");
			return;
		}
		printf("accept client sock: %d\n", client);
	}
}


void receive(int sock, int avail_bytes)
{
	int bytes = recv(sock, buf, avail_bytes, 0);
	if (bytes == 0 || bytes == -1)
	{
		close(sock);
		printf("client close or recv failed \n");
		return;
	}

	printf("recv data from sock %d: %s", sock, buf);
}


int main(int argc, char* argv[])
{
	listener = create_listener();
	if (listener == -1) return -1;

	int kq = kqueue();
	if (!register_fd(kq, listener))
	{
		printf("register_fd listener to kq failed \n");
		return -1;
	}

	printf("waiting for connection on %s %d \n", ip, port);

	wait_event(kq);
}

