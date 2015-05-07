from formatter import Formatter


class NetFormatter(Formatter):
    """
    generic formatter for icvpn network lists.
    """

    def populate_argument_parser(self, parser):
        parser.add_argument("-4",
                            dest="family",
                            action="store_const",
                            const="ipv4",
                            help="Only IPv4 networks")
        parser.add_argument("-6",
                            dest="family",
                            action="store_const",
                            const="ipv6",
                            help="Only IPv6 networks")
        parser.add_argument("-b", "--begin",
                            dest="begin",
                            help="Prefix to the list",
                            metavar="BEGIN",
                            default="")
        parser.add_argument("-e", "--end",
                            dest="end",
                            help="Suffix to the list",
                            metavar="END",
                            default="")
        parser.add_argument("-p", "--prefix",
                            dest="prefix",
                            help="Prefix for an network string",
                            metavar="PREFIX",
                            default="")
        parser.add_argument("-s", "--suffix",
                            dest="suffix",
                            help="Suffix for an network string",
                            metavar="SUFFIX",
                            default="")
        parser.add_argument("-d", "--delimiter",
                            dest="delimiter",
                            help="Delimiter between two network strings",
                            metavar="DELIM",
                            default="\n")
        parser.set_defaults(family="both")

    def generate_config(self, arguments, communities):

        family = arguments.family

        isFirst = True
        self.config.append(arguments.begin)

        for community, data in communities:

            try:
                if arguments.family == "both":
                    networks = []
                    if "ipv4" in data["networks"]:
                        networks = data["networks"]["ipv4"]
                    if "ipv6" in data["networks"]:
                        networks = networks + data["networks"]["ipv6"]
                else:
                    networks = data["networks"][family]
            except (TypeError, KeyError):
                continue

            for network in networks:
                if not isFirst:
                    self.config.append(arguments.delimiter)
                else:
                    isFirst = False
                self.config.append("{prefix}{network}{suffix}".format(
                    prefix=arguments.prefix,
                    network=network,
                    suffix=arguments.suffix))

        self.config.append(arguments.end)

    def get_config(self):
        """
        Output config string.
        """
        return "".join(self.config)
